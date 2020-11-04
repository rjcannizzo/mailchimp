-- returns mailchimp subscriber info for those no opening an email in last 1.5 years
-- and who have not spent any money
-- NOTE: only need the email address to archive or unsubscribe them

SELECT u.created, u.email, u.last_open, s.total_spent, s.order_count
from USER AS u
LEFT JOIN sales AS s
ON u.email = s.email
WHERE s.total_spent = 0
AND u.created < date('now', '-1.5 year')
AND (u.last_open IS NULL OR u.last_open < date('now', '-1.5 year'))
ORDER BY s.total_spent DESC, u.last_open DESC;