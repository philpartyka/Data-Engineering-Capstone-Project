SELECT * FROM cdw_sapp_branch;

SELECT * FROM cdw_sapp_credit_card;

SELECT * FROM cdw_sapp_customer;



SELECT cc.TIMEID, cc.TRANSACTION_VALUE, cc.TRANSACTION_TYPE, cc.CUST_CC_NO, 
c.FIRST_NAME, c.LAST_NAME,  cc.BRANCH_CODE, cc.TRANSACTION_ID 
FROM cdw_sapp_credit_card cc 
INNER JOIN cdw_sapp_customer c ON cc.CUST_SSN = c.SSN
WHERE c.CUST_ZIP = 17201
ORDER BY cc.TIMEID DESC