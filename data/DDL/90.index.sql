CREATE INDEX idx_post_code ON gis_post_code(post_code);
-- CREATE INDEX idx_city_code ON gis_city(code);  主キーなので、インデックス設定不要
CREATE INDEX idx_city_name ON gis_city(name);
CREATE INDEX idx_aza_code ON gis_aza(code);
CREATE INDEX idx_aza_name ON gis_aza(name);
