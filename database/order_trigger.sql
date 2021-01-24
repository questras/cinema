CREATE OR REPLACE FUNCTION
    order_tickets_guard() RETURNS TRIGGER
AS
$$
DECLARE
    ordered_places NUMERIC;
    all_places     NUMERIC;
    taken_places   NUMERIC;
BEGIN
    ordered_places := new.tickets_amount;
    SELECT places
    INTO all_places
    FROM hall
    WHERE hall.number =
          (
              SELECT showing.hall
              FROM showing
              WHERE showing.uuid = new.showing);

    SELECT Sum(tickets_amount)
    INTO taken_places
    FROM "order"
    WHERE "order".showing = new.showing;

    IF (all_places - taken_places < ordered_places) THEN
        -- Not enough free places for this showing.
        RETURN NULL;
    ELSE
        RETURN new;
    END IF;
END;
$$ LANGUAGE plpgsql;
CREATE TRIGGER order_tickets_trigger
    BEFORE
        INSERT
    ON "order"
    FOR EACH row
EXECUTE PROCEDURE order_tickets_guard();