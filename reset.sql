BEGIN;
SELECT setval(pg_get_serial_sequence('"questions_question"','id'), coalesce(max("id"), 1), max("id") IS NOT null) FROM "questions_question";
COMMIT;