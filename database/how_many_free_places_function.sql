CREATE OR REPLACE FUNCTION
    how_many_free_places(showing_uuid uuid) RETURNS NUMERIC
AS
$$
DECLARE
    all_places         NUMERIC;
    taken_places       NUMERIC;
    given_showing_uuid uuid;
    given_showing_hall NUMERIC;
BEGIN
    SELECT showing.uuid,
           showing.hall
    INTO given_showing_uuid,
        given_showing_hall
    FROM showing
    WHERE showing.uuid = showing_uuid;

    IF (given_showing_uuid IS NULL) THEN
        -- No such showing
        RETURN -1;
    END IF;

    -- Get all available places.
    SELECT hall.places
    INTO all_places
    FROM hall
    WHERE hall.number = given_showing_hall;

    -- Get all taken places.
    SELECT Coalesce(Sum("order".tickets_amount), 0)
    INTO taken_places
    FROM "order"
    WHERE "order".showing = given_showing_uuid;

    RETURN (all_places - taken_places);
END ;
$$ LANGUAGE plpgsql;