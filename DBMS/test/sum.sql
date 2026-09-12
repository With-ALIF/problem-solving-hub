CREATE OR REPLACE FUNCTION sum_of_three(a INT, b INT, c INT)
RETURNS INT AS $$
BEGIN
    RETURN a + b + c;
END;
$$ LANGUAGE plpgsql;

\prompt 'Enter first number: ' num1
\prompt 'Enter second number: ' num2
\prompt 'Enter third number: ' num3

SELECT sum_of_three(:num1, :num2, :num3) AS total_sum;
