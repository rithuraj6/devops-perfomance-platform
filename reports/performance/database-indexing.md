# PostgreSQL Index Performance Analysis

## Objective

Evaluate the performance impact of a B-tree index on the
`products.category` column.

## Test Environment

- Database: PostgreSQL 16.15
- Dataset: 100,002 rows
- Query:

```sql
SELECT *
FROM products
WHERE category = 'Electronics';
