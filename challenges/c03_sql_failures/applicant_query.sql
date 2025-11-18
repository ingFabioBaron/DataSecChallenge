-- ------------------------------------------------------------------------
-- SQL: Query to retrieve all the customer with more than 3 failure events
-- ------------------------------------------------------------------------
    /* select * from campaigns cam*/

    select CONCAT(cus.first_name, ' ', cus.last_name) AS customer,
           COUNT(eve.status) AS failures
      from customers cus,
           campaigns cam,
           events    eve
     where cus.id = cam.customer_id and
           eve.campaign_id = cam.id and
           --
           eve.status = 'failure'
  GROUP BY cus.id
    HAVING COUNT(eve.status) > 3
  ORDER BY failures DESC