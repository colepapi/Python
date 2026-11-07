import sys
import io

from pathlib import Path
from datetime import datetime, date
from xml.sax.saxutils import escape

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import plotly.express as px
import streamlit as st

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

from src.auth_service import authenticate
from src.expenses.expense_utils import image_type
from src.expenses.expense_config import CURRENCY
from src.expenses.expense_service import(fetch_income, fetch_receipt, fetch_expenses)

#  WINDOW
st.set_page_config(page_title="Expense Tracker", page_icon="📊", layout="wide")

LOCAL_TZ = datetime.now().astimezone().tzinfo
EXPENSE_KEYS = ["expense_id", "category", "subcategory", "recipient", "description", "amount", "spent_on", "recorded_at", "has_receipt", "funded_by",]
INCOME_KEYS = ["kind", "amount", "received_on", "note", "recorded_at"]

#  LOGIN
def show_login():
    st.title("💰 Expense Tracker Dashboard")
    st.info("Log in with the same User ID and PIN you registered with.")

    with st.form("login_form"):
        user_id = st.text_input("User ID (8 digits)", max_chars=8)
        pin = st.text_input("6-digit PIN", type="password", max_chars=6)
        submitted = st.form_submit_button("Log in")

    if submitted:
        session, message = authenticate(user_id.strip(), pin)

        if session:
            st.session_state["session"] = session
            st.rerun()
        else:
            st.error(message)


if "session" not in st.session_state:
    show_login()
    st.stop()

session = st.session_state["session"]
user_id = session["user_id"]


#  DATA (read-only from PostgreSQL)
def local_naive(series):
    return pd.to_datetime(series, utc=True).dt.tz_convert(LOCAL_TZ).dt.tz_localize(None)

def load_expenses(user_id):
    df = pd.DataFrame(fetch_expenses(user_id), columns=EXPENSE_KEYS)  
    df["Date spent"] = pd.to_datetime(df["spent_on"])
    df["Date recorded"] = local_naive(df["recorded_at"])
    df["Amount"] = df["amount"].astype(float)
    df["Recipient"] = df["recipient"].fillna("")
    df["Receipt"] = df["has_receipt"].apply(lambda has: "📎" if has else "")
    df = df.rename(
        columns={"category": "Category", "subcategory": "Subcategory", "description": "Description"}
    )
    is_return = (df["Category"] == "Money Transfer") & (df["Subcategory"] == "Receive Money")
    df["Spent"] = df["Amount"].where(df["Category"] != "Money Transfer", 0.0)
    df["Cash"] = (-df["Amount"]).where(is_return, df["Amount"]).where(df["funded_by"].isna(), 0.0)
    return df[[
        "expense_id", "Date spent", "Date recorded", "Category", "Subcategory",
        "Recipient", "Description", "Amount", "Spent", "Cash", "Receipt",
    ]]

def load_income(user_id):
    df = pd.DataFrame(fetch_income(user_id), columns=INCOME_KEYS)
    df["Date received"] = pd.to_datetime(df["received_on"])
    df["Date recorded"] = local_naive(df["recorded_at"])
    df["Amount"] = df["amount"].astype(float)
    df["Note"] = df["note"].fillna("")
    df = df.rename(columns={"kind": "Type"})
    return df[["Date received", "Date recorded", "Type", "Amount", "Note"]]

try:
    expenses = load_expenses(user_id)
    income = load_income(user_id)
except Exception as error:
    st.error(f"Could not load your data from the database: {error}")
    st.stop()

st.title("💰 Expense Tracker Dashboard")
st.info(f"Welcome, {session['full_name']}. Displaying your expenses as entered in the terminal.")

if income.empty:
    st.warning("No monthly salary is set yet. Set it in the terminal app.")

def build_expenses_pdf(export, total, full_name, filter_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), leftMargin=12 * mm, rightMargin=12 * mm, topMargin=12 * mm, bottomMargin=12 * mm, title="Expense History",)

    styles = getSampleStyleSheet()
    cell = ParagraphStyle("cell", parent=styles["BodyText"], fontSize=8, leading=10)

    story = [
        Paragraph("Finance History", styles["Title"]),
        Paragraph(
            f"{escape(full_name)} &nbsp;|&nbsp; Generated {datetime.now():%Y-%m-%d %H:%M}",
            styles["Normal"]), Paragraph(escape(filter_text), styles["Normal"]), Spacer(1, 6 * mm)]

    header = ["Date spent", "Category", "Subcategory", "Recipient", "Description", f"Amount ({CURRENCY})", "Receipt"]
    rows = [header]

    for _, r in export.iterrows():
        rows.append([
            r["Date spent"], r["Category"], r["Subcategory"], Paragraph(escape(str(r["Recipient"])), cell), Paragraph(escape(str(r["Description"])), cell),
            f"{r['Amount']:,.2f}", r["Receipt"],])

    rows.append(["", "", "", "", "TOTAL", f"{total:,.2f}", ""])

    widths = [22, 28, 50, 22, 79, 30, 22]  
    table = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2F4858")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (6, 0), (6, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, colors.HexColor("#F2F5F7")]),
        ("GRID", (0, 0), (-1, -2), 0.25, colors.HexColor("#C5CDD3")),
        ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold")]))
    story.append(table)

    def page_number(canvas, document):
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(landscape(A4)[0] - 12 * mm, 8 * mm, f"Page {document.page}")

    doc.build(story, onFirstPage=page_number, onLaterPages=page_number)
    return buffer.getvalue()

#  SIDEBAR
st.sidebar.title("Navigation")
st.sidebar.caption(f"Logged in as {session['full_name']}")
page = st.sidebar.selectbox("Choose a page", ["Dashboard", "Expenses", "Receipts"])
st.sidebar.divider()
st.sidebar.subheader("Filters")

categories = ["All"] + sorted(expenses["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Category", categories)

date_col = st.sidebar.selectbox("Filter dates by", ["Date spent", "Date recorded"], help="Date spent = when the money was actually spent. ""Date recorded = when the expense was saved to the database.",)

# Period options: All time + every month that has data (plus the current month)
current_period = pd.Timestamp.now().to_period("M")
month_periods = (set(expenses[date_col].dt.to_period("M"))| set(income["Date received"].dt.to_period("M"))| {current_period})
period_labels = {p.strftime("%B %Y"): p for p in sorted(month_periods, reverse=True)}
period_options = ["All time", "Custom range"] + list(period_labels)
selected_period = st.sidebar.selectbox("Period", period_options, index=period_options.index(current_period.strftime("%B %Y")))

range_start = range_end = None
if selected_period == "Custom range":
    picked = st.sidebar.date_input("Date range", value=(date.today().replace(day=1), date.today()))
    if isinstance(picked, (tuple, list)) and len(picked) == 2:
        range_start, range_end = picked

st.sidebar.divider()

if st.sidebar.button("🔄 Refresh data"):  
    st.rerun()

if st.sidebar.button("Log out"):
    del st.session_state["session"]
    st.rerun()

if selected_period == "Custom range" and range_start is None:
    st.info("Select both a start and an end date.")
    st.stop()

# Apply the selected filters
filtered = expenses.copy()

if selected_category != "All":
    filtered = filtered[filtered["Category"] == selected_category]

if selected_period == "Custom range":
    day = filtered[date_col].dt.normalize()
    filtered = filtered[(day >= pd.Timestamp(range_start)) & (day <= pd.Timestamp(range_end))]
elif selected_period != "All time":
    filtered = filtered[filtered[date_col].dt.to_period("M") == period_labels[selected_period]]

#  DASHBOARD
if page == "Dashboard":
    balance_period = period_labels.get(selected_period, current_period)
    month_name = balance_period.strftime("%B %Y")
    month_start = balance_period.start_time

    income_month = income[income["Date received"].dt.to_period("M") == balance_period]
    expenses_month = expenses[expenses["Date spent"].dt.to_period("M") == balance_period]

    # Carry-over: everything received minus everything spent before this month
    opening = (income.loc[income["Date received"] < month_start, "Amount"].sum() - expenses.loc[expenses["Date spent"] < month_start, "Cash"].sum())
    received = income_month["Amount"].sum()
    in_hand = opening + received - expenses_month["Cash"].sum()
    total_expenses = filtered["Spent"].sum()

    metric1, metric2, metric3, metric4 = st.columns(4, gap="medium")

    with metric1:
        with st.container(border=True):
            st.metric("Carried Over", f"{CURRENCY} {opening:,.2f}")
            st.caption("From earlier months")

    with metric2:
        with st.container(border=True):
            st.metric(f"Money Received ({month_name})", f"{CURRENCY} {received:,.2f}")

    with metric3:
        with st.container(border=True):
            st.metric("Total Expenses (filtered)", f"{CURRENCY} {total_expenses:,.2f}")

    with metric4:
        with st.container(border=True):
            st.metric(f"Money in Hand ({month_name})", f"{CURRENCY} {in_hand:,.2f}")

    st.caption(
        f"Money in hand = carried over + money received in {month_name} − everything spent in "
        f"{month_name} (all categories), by date spent."
    )

    st.divider()

    #  MAIN CHART LAYOUT
    left_col, right_col = st.columns([1.1, 1], gap="large")

    category_totals = (filtered.groupby("Category", as_index=False)["Spent"].sum().rename(columns={"Spent": "Amount"}))
    category_totals = category_totals[category_totals["Amount"] > 0]

    with left_col:
        with st.container(border=True):
            st.subheader("Expenses by Category")

            if not filtered.empty:
                bar = px.bar(category_totals, x="Category", y="Amount", labels={"Category": "Expense Category", "Amount": f"Amount ({CURRENCY})"})
                bar.update_layout(height=320, margin=dict(t=20, b=20, l=20, r=20))
                st.plotly_chart(bar, width="stretch")
            else:
                st.info("No expenses match these filters.")

    with right_col:
        with st.container(border=True):
            st.subheader("Spending Distribution")

            if not filtered.empty:
                donut = px.pie(category_totals, names="Category", values="Amount", hole=0.55)
                donut.update_traces(textinfo="percent", hovertemplate=f"%{{label}}<br> {CURRENCY} %{{value:,.2f}} <extra></extra>")
                donut.update_layout(height=320, margin=dict(t=20, b=20, l=10, r=10), showlegend=True)
                st.plotly_chart(donut, width="stretch")
            else:
                st.info("No expenses match these filters.")

    # RUNNING BALANCE: shows money running out and being topped up
    with st.container(border=True):
        st.subheader(f"Money in hand through {month_name}")

        first_day = balance_period.start_time
        last_day = min(balance_period.end_time.normalize(), pd.Timestamp.now().normalize())
        days = pd.date_range(first_day, last_day)

        spent_daily = expenses_month.groupby("Date spent")["Cash"].sum().reindex(days, fill_value=0.0)
        received_daily = income_month.groupby("Date received")["Amount"].sum().reindex(days, fill_value=0.0)
        running = opening + received_daily.cumsum() - spent_daily.cumsum()

        line = px.line(pd.DataFrame({"Date": days, "Balance": running.values}), x="Date", y="Balance", markers=True, line_shape="hv", labels={"Balance": f"Money in hand ({CURRENCY})"})
        line.add_hline(y=0, line_dash="dot")
        line.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(line, width="stretch")
        st.caption("Drops are spending (by date spent). Jumps up are money received (by date received).")

#  EXPENSE HISTORY TABLE + RECEIPTS
elif page == "Expenses":
    st.subheader("Expense History")
    st.caption(
        f"{len(filtered)} expense(s), filtered by **{date_col.lower()}**. "
        "Resize the table using its bottom-right corner. Drag column borders to adjust column widths."
    )

    if filtered.empty:
        st.info("No expenses match these filters.")
    else:
        display_data = filtered.sort_values(date_col, ascending=False).copy()
        table = display_data.drop(columns=["expense_id", "Spent", "Cash"])
        table["Date spent"] = table["Date spent"].dt.strftime("%Y-%m-%d")
        table["Date recorded"] = table["Date recorded"].dt.strftime("%Y-%m-%d %H:%M")

        st.dataframe(table, width="stretch", height=350, hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn(f"Amount ({CURRENCY})", format="%.2f"),
                "Description": st.column_config.TextColumn("Description", width="large")
            })

        export = table.copy()
        export["Receipt"] = export["Receipt"].map(lambda has: "Yes" if has else "")

        if selected_period == "Custom range":
            period_text = f"{range_start:%Y-%m-%d} to {range_end:%Y-%m-%d}"
        else:
            period_text = selected_period

        filter_text = (
            f"Category: {selected_category} | Period: {period_text} | {len(export)} expense(s)")
        stamp = f"{date.today():%Y-%m-%d}"

        csv_col, pdf_col, _ = st.columns([1, 1, 4])

        with csv_col:
            st.download_button("⬇ Download CSV", data=export.to_csv(index=False).encode("utf-8-sig"), file_name=f"expense_history_{stamp}.csv", mime="text/csv")

        with pdf_col:
            st.download_button("⬇ Download PDF", data=build_expenses_pdf(export, display_data["Spent"].sum(), session["full_name"], filter_text), file_name=f"expense_history_{stamp}.pdf", mime="application/pdf")

#  RECEIPTS SECTION
elif page == "Receipts":
    display_data = filtered.sort_values(date_col, ascending=False).copy()

    with_receipts = display_data[display_data["Receipt"] != ""]

    if not with_receipts.empty:
        st.subheader("Receipts")

        labels = {
            int(row["expense_id"]): (
                f"{row['Date spent']:%Y-%m-%d}                      {row['Description']}                            {CURRENCY} {row['Amount']:,.2f}"
            )
            for _, row in with_receipts.iterrows()
        }

        chosen = st.selectbox("Choose an expense", list(labels), format_func=labels.get)
        data = fetch_receipt(user_id, chosen)  

        if data:
            mime_type = image_type(data) or "image/jpeg"
            extension = "png" if mime_type == "image/png" else "jpg"
            st.image(data, caption=labels[chosen], width=420)
            st.download_button("⬇ Download receipt", data=data, file_name=f"receipt_{chosen}.{extension}", mime=mime_type)


#  MONEY RECEIVED
elif page == "Money received":
    st.subheader("Money Received")
    st.caption("Salary and top-ups, with the date each amount arrived and the date it was recorded.")

    if income.empty:
        st.info("No money received has been recorded yet.")
    else:
        table = income.copy()
        table["Date received"] = table["Date received"].dt.strftime("%Y-%m-%d")
        table["Date recorded"] = table["Date recorded"].dt.strftime("%Y-%m-%d %H:%M")

        st.dataframe(table, width="stretch", height=350, hide_index=True,
            column_config={
                "Amount": st.column_config.NumberColumn(f"Amount ({CURRENCY})", format="%.2f"),
            }
        )