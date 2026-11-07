CREATE TABLE IF NOT EXISTS users (
    user_id         CHAR(8)      PRIMARY KEY,
    full_name       TEXT         NOT NULL,
    email           TEXT         NOT NULL UNIQUE,
    pin_hash        TEXT         NOT NULL,
    failed_attempts INTEGER      NOT NULL DEFAULT 0 CHECK (failed_attempts >= 0),
    locked_until    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),

    CONSTRAINT users_user_id_format CHECK (user_id ~ '^[0-9]{8}$')
);


CREATE TABLE IF NOT EXISTS expenses (
    expense_id     BIGSERIAL PRIMARY KEY,
    user_id        CHAR(8) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    category       TEXT NOT NULL,
    subcategory    TEXT NOT NULL,
    description    TEXT NOT NULL,
    amount         NUMERIC(14,2) NOT NULL CHECK (amount >= 0),
    food_cost      NUMERIC(14,2),
    delivery_fee   NUMERIC(14,2),
    recorded_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    spent_on       DATE NOT NULL DEFAULT CURRENT_DATE,
    receipt_image  BYTEA,
    recipient      TEXT,
    settled_by     BIGINT REFERENCES expenses(expense_id) ON DELETE SET NULL,
    funded_by      BIGINT REFERENCES expenses(expense_id) ON DELETE CASCADE
);

-- bring databases created by earlier versions up to date
CREATE INDEX IF NOT EXISTS idx_expenses_user_time  ON expenses (user_id, recorded_at DESC);
CREATE INDEX IF NOT EXISTS idx_expenses_user_spent ON expenses (user_id, spent_on DESC);


CREATE TABLE IF NOT EXISTS income (
    income_id    BIGSERIAL PRIMARY KEY,
    user_id      CHAR(8) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    kind         TEXT NOT NULL DEFAULT 'Salary',
    amount       NUMERIC(14,2) NOT NULL CHECK (amount > 0),
    received_on  DATE NOT NULL DEFAULT CURRENT_DATE,
    note         TEXT,
    recorded_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_income_user_received ON income (user_id, received_on DESC);

-- one-time: old "Returned" income rows become Receive Money expenses
DO $$
DECLARE
    r RECORD;
    new_id BIGINT;
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name = 'income' AND column_name = 'transfer_id'
    ) THEN
        FOR r IN
            SELECT i.*, e.recipient AS recipient
            FROM income i LEFT JOIN expenses e ON e.expense_id = i.transfer_id
            WHERE i.kind = 'Returned'
        LOOP
            INSERT INTO expenses
                (user_id, category, subcategory, recipient, description, amount, spent_on, recorded_at)
            VALUES (r.user_id, 'Money Transfer', 'Receive Money', r.recipient,
                    COALESCE(r.note, 'Returned money'), r.amount, r.received_on, r.recorded_at)
            RETURNING expense_id INTO new_id;

            UPDATE expenses SET settled_by = new_id WHERE expense_id = r.transfer_id;
        END LOOP;

        DELETE FROM income WHERE kind = 'Returned';
        DROP INDEX IF EXISTS idx_income_one_return;
        ALTER TABLE income DROP COLUMN transfer_id;
    END IF;
END $$;

-- one-time: returns that used expenses.transfer_id now use settled_by on the send
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_schema = current_schema()
          AND table_name = 'expenses' AND column_name = 'transfer_id'
    ) THEN
        UPDATE expenses s SET settled_by = r.expense_id
        FROM expenses r
        WHERE r.transfer_id = s.expense_id AND s.settled_by IS NULL;

        DROP INDEX IF EXISTS idx_expenses_one_return;
        ALTER TABLE expenses DROP COLUMN transfer_id;
    END IF;
END $$;