
CREATE OR REPLACE VIEW vw_temperatura_media AS
SELECT
    room_id,
    ROUND(AVG(temp)::numeric, 2) AS temperatura_media,
    MIN(temp) AS temperatura_minima,
    MAX(temp) AS temperatura_maxima,
    COUNT(*) AS total_leituras
FROM leituras_temperatura
GROUP BY room_id;


CREATE OR REPLACE VIEW vw_temperaturas_extremas AS
SELECT
    id,
    room_id,
    noted_date,
    temp,
    out_in
FROM leituras_temperatura
WHERE temp = (SELECT MAX(temp) FROM leituras_temperatura)
   OR temp = (SELECT MIN(temp) FROM leituras_temperatura);


CREATE OR REPLACE VIEW vw_resumo_diario AS
SELECT
    CAST(noted_date AS DATE) AS data_leitura,
    ROUND(AVG(temp)::numeric, 2) AS temperatura_media,
    MIN(temp) AS temperatura_minima,
    MAX(temp) AS temperatura_maxima,
    COUNT(*) AS total_leituras
FROM leituras_temperatura
GROUP BY CAST(noted_date AS DATE);
