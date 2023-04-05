import http from '../../utils/http';
import { SINGLE_TEXT_MAPPING_URL } from '../../utils/constant/url';

export const mapSingleText = (code) => http.get(SINGLE_TEXT_MAPPING_URL, { code });
