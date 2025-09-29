import pandas as pd
import io
import math
import streamlit as st # Streamlit 임포트 추가

EUR_TO_USD = 1.1082

st.set_page_config(page_title="Extra Calculator", layout="wide")

# -----------------------
# Raw data sections (CSV strings) - from user's provided data
# -----------------------

# 1) Non-EU coating table (coating Mxxx, t_from, t_to, extra) - USD
non_eu_coating_csv = r"""coating,t_min,t_max,extra
M090,0.376,0.425,45
M090,0.426,0.475,40
M090,0.476,0.525,38
M090,0.526,0.575,19
M090,0.576,0.65,19
M090,0.651,0.75,16
M090,0.751,0.85,14
M090,0.851,0.95,12
M090,0.951,0.999,10
M090,1,99.999,0
M090,1.001,99.999,0
M100,0.376,0.425,45
M100,0.426,0.475,40
M100,0.476,0.525,38
M100,0.526,0.575,19
M100,0.576,0.65,19
M100,0.651,0.75,16
M100,0.751,0.85,14
M100,0.851,0.95,12
M100,0.951,0.999,10
M100,1,99.999,0
M100,1.001,99.999,0
M110,0.376,0.425,45
M110,0.426,0.475,40
M110,0.476,0.525,38
M110,0.526,0.575,19
M110,0.576,0.65,19
M110,0.651,0.75,16
M110,0.751,0.85,14
M110,0.851,0.95,12
M110,0.951,0.999,10
M110,1,99.999,0
M110,1.001,99.999,0
M120,0.376,0.425,45
M120,0.426,0.475,40
M120,0.476,0.525,38
M120,0.526,0.575,19
M120,0.576,0.65,19
M120,0.651,0.75,16
M120,0.751,0.85,14
M120,0.851,0.95,12
M120,0.951,0.999,10
M120,1,99.999,0
M120,1.001,99.999,0
M140,0.376,0.425,55
M140,0.426,0.475,50
M140,0.476,0.525,48
M140,0.526,0.575,29
M140,0.576,0.65,29
M140,0.651,0.75,26
M140,0.751,0.85,24
M140,0.851,0.95,22
M140,0.951,0.999,20
M140,1,99.999,10
M180,0.376,0.425,65
M180,0.426,0.475,60
M180,0.476,0.525,58
M180,0.526,0.575,39
M180,0.576,0.65,39
M180,0.651,0.75,36
M180,0.751,0.85,34
M180,0.851,0.95,32
M180,0.951,0.999,30
M180,1,99.999,20
M220,0.376,0.425,75
M220,0.426,0.475,70
M220,0.476,0.525,68
M220,0.526,0.575,49
M220,0.576,0.65,49
M220,0.651,0.75,46
M220,0.751,0.85,44
M220,0.851,0.95,42
M220,0.951,0.999,40
M220,1,99.999,30
M250,0.376,0.425,80
M250,0.426,0.475,75
M250,0.476,0.525,73
M250,0.526,0.575,54
M250,0.576,0.65,54
M250,0.651,0.75,51
M250,0.751,0.85,49
M250,0.851,0.95,47
M250,0.951,0.999,45
M250,1,99.999,35
M275,0.376,0.425,85
M275,0.426,0.475,80
M275,0.476,0.525,78
M275,0.526,0.575,59
M275,0.576,0.65,59
M275,0.651,0.75,56
M275,0.751,0.85,54
M275,0.851,0.95,52
M275,0.951,0.999,50
M275,1,99.999,40
M300,0.376,0.425,85
M300,0.426,0.475,80
M300,0.476,0.525,78
M300,0.526,0.575,59
M300,0.576,0.65,59
M300,0.651,0.75,56
M300,0.751,0.85,54
M300,0.851,0.95,52
M300,0.951,0.999,50
M300,1,99.999,40
M310,0.376,0.425,85
M310,0.426,0.475,80
M310,0.476,0.525,78
M310,0.526,0.575,59
M310,0.576,0.65,59
M310,0.651,0.75,56
M310,0.751,0.85,54
M310,0.851,0.95,52
M310,0.951,0.999,50
M310,1,100,40
M350,0.376,0.425,95
M350,0.426,0.475,90
M350,0.476,0.525,88
M350,0.526,0.575,69
M350,0.576,0.65,69
M350,0.651,0.75,66
M350,0.751,0.85,64
M350,0.851,0.95,62
M350,0.951,0.999,60
M350,1,99.999,50
M400,0.376,0.425,105
M400,0.426,0.475,100
M400,0.476,0.525,98
M400,0.526,0.575,79
M400,0.576,0.65,79
M400,0.651,0.75,76
M400,0.751,0.85,74
M400,0.851,0.95,72
M400,0.951,0.999,70
M400,1,99.999,60
M430,0.426,0.475,118
M430,0.476,0.525,116
M430,0.526,0.575,97
M430,0.576,0.65,97
M430,0.651,0.75,94
M430,0.751,0.85,92
M430,0.851,0.95,90
M430,0.951,0.999,88
M430,1,99.99,78
M450,0.376,0.425,115
M450,0.426,0.475,110
M450,0.476,0.525,108
M450,0.526,0.575,89
M450,0.576,0.65,89
M450,0.651,0.75,86
M450,0.751,0.85,84
M450,0.851,0.95,82
M450,0.951,0.999,80
M450,1,99.999,70
"""

# 2) Non-EU grade extras (USD)
non_eu_grade_csv = r"""grade,extra
EN-S350GD,18
EN-S390GD,18
EN-S420GD,25
EN-S450GD,25
PM3HT340R,8
PM3HT400R,16
PM3HT440C,18
PM3HT440C2,18
PM3HT490C,18
PM3HT490C2,18
PM3HT540C,25
PM3HT540C2,25
A1046H-SS255,8
A1046H-SS275,16
A1046H-SS341,18
A1046H-H340,18
A1046H-S341,18
A1046H-SS380,18
A1046H-SS410,25
POSMAC-C,0
POSMAC-D,23
POSMAC-340,8
POSMAC-380,8
POSMAC-400,16
POSMAC-440,18
POSMAC-490,18
POSMAC-540,25
PM3HT270CQ,0
PM3HT270DQ,23
EN-DX51D,0
EN-DX53D,23
EN-S220GD,0
EN-S250GD,8
EN-S280GD,16
EN-S320GD,17
A1046H-CSA,0
A1046H-CSB,0
A1046H-FSA,23
EN-S550GD,87
"""

# 3) Non-EU width extra (from,to,extra) - USD
non_eu_width_csv = r"""w_min,w_max,extra
0,770.9,20
771,870.9,15
871,899.9,10
900,1420.9,0
1421,1549.9,5
1550,9999.9,15
"""

# 4) EU grade extras (euro)
eu_grade_csv = r"""grade,extra_eur
EN-DX51DHM,0
EN-S220GDHM,0
EN-S250GDHM,5
EN-S280GDHM,15
EN-S320GDHM,23
EN-S350GDHM,40
EN-S390GDHM,50
EN-S420GDHM,56
EN-S450GDHM,56
EN-S550GDHM,58
PM3HY550B,58
"""

# 5) EU coating by thickness (euro)
eu_coating_csv = r"""coating,t_min,t_max,extra_eur
M090,0.45,0.499,30
M090,0.5,0.549,30
M090,0.55,0.599,30
M090,0.6,0.699,25
M090,0.7,0.799,20
M090,0.8,0.899,20
M090,0.9,0.999,15
M090,1,1.249,15
M090,1.25,1.499,10
M090,1.5,1.999,10
M090,2,2.499,10
M090,2.5,99.9,10
M100,0.45,0.499,30
M100,0.5,0.549,30
M100,0.55,0.599,30
M100,0.6,0.699,25
M100,0.7,0.799,20
M100,0.8,0.899,20
M100,0.9,0.999,15
M100,1,1.249,15
M100,1.25,1.499,10
M100,1.5,1.999,10
M100,2,2.499,10
M100,2.5,99.9,10
M120,0.45,0.499,47
M120,0.5,0.549,45
M120,0.55,0.599,44
M120,0.6,0.699,43
M120,0.7,0.799,35
M120,0.8,0.899,29
M120,0.9,0.999,28
M120,1,1.249,22
M120,1.25,1.499,21
M120,1.5,1.999,16
M120,2,2.499,14
M120,2.5,99.9,13
M140,0.45,0.499,59
M140,0.5,0.549,57
M140,0.55,0.599,54
M140,0.6,0.699,51
M140,0.7,0.799,43
M140,0.8,0.899,36
M140,0.9,0.999,34
M140,1,1.249,28
M140,1.25,1.499,26
M140,1.5,1.999,21
M140,2,2.499,18
M140,2.5,99.9,15
M175,0.45,0.499,71
M175,0.5,0.549,67
M175,0.55,0.599,64
M175,0.6,0.699,60
M175,0.7,0.799,50
M175,0.8,0.899,43
M175,0.9,0.999,39
M175,1,1.249,34
M175,1.25,1.499,30
M175,1.5,1.999,26
M175,2,2.499,22
M175,2.5,99.9,18
M180,0.45,0.499,71
M180,0.5,0.549,67
M180,0.55,0.599,64
M180,0.6,0.699,60
M180,0.7,0.799,50
M180,0.8,0.899,43
M180,0.9,0.999,39
M180,1,1.249,34
M180,1.25,1.499,30
M180,1.5,1.999,26
M180,2,2.499,22
M180,2.5,99.9,18
M195,0.45,0.499,81
M195,0.5,0.549,77
M195,0.55,0.599,70
M195,0.6,0.699,67
M195,0.7,0.799,59
M195,0.8,0.899,54
M195,0.9,0.999,48
M195,1,1.249,42
M195,1.25,1.499,39
M195,1.5,1.999,34
M195,2,2.499,28
M195,2.5,99.9,25
M200,0.45,0.499,81
M200,0.5,0.549,77
M200,0.55,0.599,70
M200,0.6,0.699,67
M200,0.7,0.799,59
M200,0.8,0.899,54
M200,0.9,0.999,48
M200,1,1.249,42
M200,1.25,1.499,39
M200,1.5,1.999,34
M200,2,2.499,28
M200,2.5,99.9,25
M220,0.45,0.499,88
M220,0.5,0.549,83
M220,0.55,0.599,77
M220,0.6,0.699,73
M220,0.7,0.799,66
M220,0.8,0.899,61
M220,0.9,0.999,55
M220,1,1.249,50
M220,1.25,1.499,46
M220,1.5,1.999,42
M220,2,2.499,37
M220,2.5,99.9,33
M250,0.45,0.499,94
M250,0.5,0.549,89
M250,0.55,0.599,83
M250,0.6,0.699,78
M250,0.7,0.799,72
M250,0.8,0.899,67
M250,0.9,0.999,62
M250,1,1.249,57
M250,1.25,1.499,53
M250,1.5,1.999,50
M250,2,2.499,45
M250,2.5,99.9,42
M275,0.45,0.499,109
M275,0.5,0.549,101
M275,0.55,0.599,95
M275,0.6,0.699,88
M275,0.7,0.799,80.5
M275,0.8,0.899,74.5
M275,0.9,0.999,68.5
M275,1,1.249,65
M275,1.25,1.499,58
M275,1.5,1.999,54
M275,2,2.499,48
M275,2.5,99.9,45
M300,0.45,0.499,123
M300,0.5,0.549,112
M300,0.55,0.599,106
M300,0.6,0.699,98
M300,0.7,0.799,88
M300,0.8,0.899,82
M300,0.9,0.999,75
M300,1,1.249,72
M300,1.25,1.499,63
M300,1.5,1.999,57
M300,2,2.499,50
M300,2.5,99.9,48
M310,0.45,0.499,123
M310,0.5,0.549,112
M310,0.55,0.599,106
M310,0.6,0.699,98
M310,0.7,0.799,88
M310,0.8,0.899,82
M310,0.9,0.999,75
M310,1,1.249,72
M310,1.25,1.499,63
M310,1.5,1.999,57
M310,2,2.499,50
M310,2.5,99.9,48
M350,0.45,0.499,157
M350,0.5,0.549,141
M350,0.55,0.599,134
M350,0.6,0.699,125
M350,0.7,0.799,122.5
M350,0.8,0.899,113
M350,0.9,0.999,108
M350,1,1.249,104
M350,1.25,1.499,99
M350,1.5,1.999,85
M350,2,2.499,67
M350,2.5,99.9,65
M400,0.45,0.499,179
M400,0.5,0.549,162
M400,0.55,0.599,152.5
M400,0.6,0.699,143
M400,0.7,0.799,140.5
M400,0.8,0.899,128.5
M400,0.9,0.999,123
M400,1,1.249,118
M400,1.25,1.499,113
M400,1.5,1.999,97
M400,2,2.499,76
M400,2.5,99.9,74.5
M430,0.45,0.499,193
M430,0.5,0.549,174
M430,0.55,0.599,164
M430,0.6,0.699,153
M430,0.7,0.799,151
M430,0.8,0.899,139
M430,0.9,0.999,132
M430,1,1.249,127
M430,1.25,1.499,122
M430,1.5,1.999,104
M430,2,2.499,82
M430,2.5,99.9,80.5
M630,0.45,0.499,246
M630,0.5,0.549,224
M630,0.55,0.599,212
M630,0.6,0.699,196
M630,0.7,0.799,176
M630,0.8,0.899,164
M630,0.9,0.999,150
M630,1,1.249,144
M630,1.25,1.499,126
M630,1.5,1.999,114
M630,2,2.499,100
M630,2.5,99.9,96
"""

# 6) EU thickness-width combination table (euro)
eu_thick_width_csv = r"""t_min,t_max,w_min,w_max,extra_eur
0.45,0.49,600,699.9,163
0.5,0.54,600,699.9,152
0.5,0.59,600,699.9,147
0.6,0.69,600,699.9,132
0.7,0.79,600,699.9,123
0.8,0.89,600,699.9,105
0.9,0.99,600,699.9,102
1,1.24,600,699.9,93
1.25,1.49,600,699.9,86
1.5,1.99,600,699.9,79
2,2.49,600,699.9,65
2.5,99.999,600,699.9,64
0.45,0.49,700,799.9,143
0.5,0.54,700,799.9,138
0.5,0.59,700,799.9,129
0.6,0.69,700,799.9,112
0.7,0.79,700,799.9,106
0.8,0.89,700,799.9,87
0.9,0.99,700,799.9,86
1,1.24,700,799.9,78
1.25,1.49,700,799.9,73
1.5,1.99,700,799.9,66
2,2.49,700,799.9,49
2.5,99.999,700,799.9,49
0.45,0.49,800,899.9,123
0.5,0.54,800,899.9,111
0.5,0.59,800,899.9,105
0.6,0.69,800,899.9,88
0.7,0.79,800,899.9,84
0.8,0.89,800,899.9,75
0.9,0.99,800,899.9,71
1,1.24,800,899.9,63
1.25,1.49,800,899.9,58
1.5,1.99,800,899.9,51
2,2.49,800,899.9,36
2.5,99.999,800,899.9,36
0.45,0.49,900,1099.9,106
0.5,0.54,900,1099.9,89
0.5,0.59,900,1099.9,88
0.6,0.69,900,1099.9,76
0.7,0.79,900,1099.9,72
0.8,0.89,900,1099.9,62
0.9,0.99,900,1099.9,61
1,1.24,900,1099.9,53
1.25,1.49,900,1099.9,45
1.5,1.99,900,1099.9,38
2,2.49,900,1099.9,26
2.5,99.999,900,1099.9,25
0.45,0.49,1100,1299.9,99
0.5,0.54,1100,1299.9,78
0.5,0.59,1100,1299.9,75
0.6,0.69,1100,1299.9,66
0.7,0.79,1100,1299.9,62
0.8,0.89,1100,1299.9,52
0.9,0.99,1100,1299.9,52
1,1.24,1100,1299.9,45
1.25,1.49,1100,1299.9,38
1.5,1.99,1100,1299.9,31
2,2.49,1100,1299.9,19
2.5,99.999,1100,1299.9,19
0.45,0.49,1300,1850,99
0.5,0.54,1300,1850,78
0.5,0.59,1300,1850,75
0.6,0.69,1300,1850,66
0.7,0.79,1300,1850,62
0.8,0.89,1300,1850,52
0.9,0.99,1300,1850,52
1,1.24,1300,1850,45
1.25,1.49,1300,1850,38
1.5,1.99,1300,1850,31
2,2.49,1300,1850,18
2.5,99.999,1300,1850,18
"""
# -----------------------
# Streamlit 최적화를 위한 데이터 로딩 함수 (Caching 사용)
# -----------------------
@st.cache_data
def load_all_data():
    """모든 CSV 문자열을 DataFrame으로 변환하고 Streamlit 캐시에 저장합니다."""
    
    # 기존 파일의 df_from_csv_string 함수는 이 내부에 통합됩니다.
    def df_from_csv_string(s):
        # M310의 마지막 행 t_max 값 오류 수정 (100 -> 99.999)
        # 이스케이프 문자열 r"""을 사용하므로, \r\n는 이미 처리됨.
        s = s.replace('M310,1,100,40', 'M310,1,99.999,40')
        return pd.read_csv(io.StringIO(s.strip()))

    df_non_eu_coating = df_from_csv_string(non_eu_coating_csv)
    df_non_eu_grade = df_from_csv_string(non_eu_grade_csv)
    df_non_eu_width = df_from_csv_string(non_eu_width_csv)
    df_eu_grade = df_from_csv_string(eu_grade_csv)
    df_eu_coating = df_from_csv_string(eu_coating_csv)
    df_eu_tw = df_from_csv_string(eu_thick_width_csv)

    return (df_non_eu_coating, df_non_eu_grade, df_non_eu_width,
            df_eu_grade, df_eu_coating, df_eu_tw)

# 앱 시작 시 데이터를 로드하고 캐시합니다.
(df_non_eu_coating, df_non_eu_grade, df_non_eu_width,
 df_eu_grade, df_eu_coating, df_eu_tw) = load_all_data()

# -----------------------
# Normalization helpers & Matching functions
# -----------------------
# *주의*: 이 부분은 기존 파일의 코드를 변경 없이 그대로 복사합니다. 
#       (normalize_coating, normalize_grade, find_grade_extra_non_eu, 
#        find_grade_extra_eu, match_non_eu_coating, match_non_eu_width, 
#        match_eu_coating, match_eu_thick_width, match_non_eu_grade, match_eu_grade)
#        **여기에 모두 복사했다고 가정합니다.**
def normalize_coating(code: str) -> str:
    if not isinstance(code, str):
        return ""
    code = code.strip().upper()
    code = code.replace("ZM", "M")  # ZM -> M
    return code

def normalize_grade(g: str) -> str:
    if not isinstance(g, str):
        return ""
    s = g.strip().upper()
    # common shortenings: remove spaces, handle forms like "350GD" -> "EN-S350GDHM" is specific mapping but
    # we'll try matching in decreasing strictness:
    s = s.replace(" ", "")
    # If the exact grade exists in either table, return s
    return s

# Grade matching with flexible patterns:
def find_grade_extra_non_eu(grade_input):
    if pd.isna(grade_input):
        return 0
    g = normalize_grade(grade_input)
    # direct match
    rows = df_non_eu_grade[df_non_eu_grade['grade'].str.upper() == g]
    if not rows.empty:
        return float(rows.iloc[0]['extra'])
    # try variations: if input is like "S350GD" or "350GD", try to match EN-S350GDHM or EN-S350GDHM variants
    # extract numeric part
    import re
    num_match = re.search(r'(\d{3,4})', g)
    if num_match:
        num = num_match.group(1)
        # prefer EN-S{num}GD
        candidates = [
            f"EN-S{num}GD",
            f"S{num}GD",
            f"{num}GD",
            f"S{num}GD",
            f"{num}GD",
            f"A1046H-S{num}"
        ]
        for c in candidates:
            rows = df_non_eu_grade[df_non_eu_grade['grade'].str.upper() == c]
            if not rows.empty:
                return float(rows.iloc[0]['extra'])
    # if startswith PM3HT... match prefix
    for _, r in df_non_eu_grade.iterrows():
        if g.startswith(str(r['grade']).split('-')[0].upper()):
            # exact prefix match
            if str(r['grade']).upper().startswith(g):
                return float(r['extra'])
    return 0

def find_grade_extra_eu(grade_input):
    if pd.isna(grade_input):
        return 0
    g = normalize_grade(grade_input)
    rows = df_eu_grade[df_eu_grade['grade'].str.upper() == g]
    if not rows.empty:
        return float(rows.iloc[0]['extra_eur'])
    # fallback by numeric YP
    import re
    num_match = re.search(r'(\d{3,4})', g)
    if num_match:
        num = num_match.group(1)
        candidates = [f"EN-S{num}GD", f"S{num}GD", f"{num}GDHM", f"S{num}GD", f"{num}GD"]
        for c in candidates:
            rows = df_eu_grade[df_eu_grade['grade'].str.upper() == c]
            if not rows.empty:
                return float(rows.iloc[0]['extra_eur'])
    return 0

# -----------------------
# Matching functions
# -----------------------

def match_non_eu_coating(coating, thickness):
    coating = normalize_coating(coating)
    if coating == "":
        return 0.0
    # find rows with same coating and t_min <= thickness <= t_max
    df = df_non_eu_coating[df_non_eu_coating['coating'].str.upper() == coating]
    if df.empty:
        return 0.0
    for _, r in df.iterrows():
        if float(r['t_min']) <= thickness <= float(r['t_max']):
            return float(r['extra'])
    return 0.0

def match_non_eu_width(width):
    for _, r in df_non_eu_width.iterrows():
        if float(r['w_min']) <= width <= float(r['w_max']):
            return float(r['extra'])
    return 0.0

def match_eu_coating(coating, thickness):
    coating = normalize_coating(coating)
    if coating == "":
        return 0.0
    df = df_eu_coating[df_eu_coating['coating'].str.upper() == coating]
    if df.empty:
        return 0.0
    for _, r in df.iterrows():
        if float(r['t_min']) <= thickness <= float(r['t_max']):
            return float(r['extra_eur'])
    return 0.0

def match_eu_thick_width(thickness, width):
    # eu_thick_width: t_min,t_max,w_min,w_max,extra_eur
    for _, r in df_eu_tw.iterrows():
        if float(r['t_min']) <= thickness <= float(r['t_max']) and float(r['w_min']) <= width <= float(r['w_max']):
            return float(r['extra_eur'])
    return 0.0

def match_non_eu_grade(grade):
    return find_grade_extra_non_eu(grade)

def match_eu_grade(grade):
    return find_grade_extra_eu(grade)

# -----------------------
# Main calculation API
# -----------------------
def calculate_extra(grade, coating, thickness, width=None, region="non-EU"):
    """
    :param grade: str
    :param coating: str (e.g. M120 or ZM120)
    :param thickness: float (mm)
    :param width: float (mm) or None -> default 1200
    :param region: "EU" or "non-EU" (case-insensitive)
    :return: dict {total_usd, breakdown}
    """
    if width is None or (isinstance(width, str) and width.strip()==""):
        width = 1200.0
    width = float(width)
    region = region.strip().upper()
    if region not in ("EU", "NON-EU"):
        raise ValueError("Region must be 'EU' or 'non-EU'")

    if region == "NON-EU":
        c_extra = match_non_eu_coating(coating, thickness)
        g_extra = match_non_eu_grade(grade)
        w_extra = match_non_eu_width(width)
        total = c_extra + g_extra + w_extra
        return {
            "total_usd_per_mt": round(float(total), 2),
            "breakdown": {
                "coating_extra_usd": round(float(c_extra),2),
                "grade_extra_usd": round(float(g_extra),2),
                "width_extra_usd": round(float(w_extra),2)
            },
            "notes": "non-EU: all values USD"
        }
    else:  # EU
        # all euro table values then convert
        c_extra_eur = match_eu_coating(coating, thickness)
        g_extra_eur = match_eu_grade(grade)
        tw_extra_eur = match_eu_thick_width(thickness, width)
        total_eur = c_extra_eur + g_extra_eur + tw_extra_eur
        total_usd = total_eur * EUR_TO_USD
        total_usd_rounded = round(total_usd)
        return {
            "total_usd_per_mt": total_usd_rounded,
            "breakdown": {
                "coating_extra_eur": round(float(c_extra_eur), 2),
                "grade_extra_eur": round(float(g_extra_eur), 2),
                "thick_width_extra_eur": round(float(tw_extra_eur), 2),
                "sum_eur": round(float(total_eur), 2),
                "exchange_rate": EUR_TO_USD
            },
            "notes": "EU: extras were in EUR then converted to USD (rounded to integer)"
        }

# -----------------------
# Main calculation API (calculate_extra 함수)
# -----------------------
# *주의*: 이 부분도 기존 파일의 calculate_extra 함수를 변경 없이 그대로 복사합니다.

# -----------------------
# 선택 위젯을 위한 등급 목록 준비
# -----------------------
all_grades = set()
# 대문자화하여 목록을 만듭니다.
all_grades.update(df_non_eu_grade['grade'].str.upper().tolist())
all_grades.update(df_eu_grade['grade'].str.upper().tolist())

# 등급을 정렬하고 리스트로 변환합니다.
GRADE_OPTIONS = sorted(list(all_grades))

# 기본값 설정
DEFAULT_GRADE = 'EN-S350GD' 

# -----------------------
# Streamlit App Logic (이 부분이 핵심입니다.)
# -----------------------

st.title("💰 PosMAC EXTRA 비용 계산기 (Extra Calculator)")
st.caption("Grade, 코팅량, 사이즈에 따른 USD/MT 추가 비용을 계산합니다.")

# 1. 지역 선택
region = st.radio(
    "1. 지역을 선택하세요:",
    ("non-EU", "EU"),
    # captions 라인 제거됨
    horizontal=True
)
# 설명은 st.caption()을 사용해 별도로 표시할 수 있습니다.
st.caption("non-EU: USD 기준 | EU: EUR 기준 후 USD 환산 (환율: 1.1082)")

# 2. 필수 입력값 섹션
col1, col2, col3, col4 = st.columns(4)

with col1:
# ---------------------------------------------
    # Grade 등급 입력 (자동 완성처럼 작동하는 Selectbox)
    # ---------------------------------------------
    # st.selectbox는 목록이 길 경우 사용자가 입력할 때마다 목록을 필터링해 줍니다.
    grade_input = st.selectbox(
        "2. Grade 규격",
        GRADE_OPTIONS,
        # 기본값 설정: GRADE_OPTIONS 리스트에서 'EN-S350GD'의 인덱스를 찾아 지정합니다.
        index=GRADE_OPTIONS.index(DEFAULT_GRADE) if DEFAULT_GRADE in GRADE_OPTIONS else 0
    )
with col2:
    coating_input = st.text_input("3. Coating 코팅", value="M310")
with col3:
    # 너비와 두께 입력은 슬라이더 대신 숫자 입력창을 사용하는 것이 정확도에 유리
    thickness_input = st.number_input("4. Thickness 두께 (mm)", min_value=0.3, max_value=10.0, value=2.0, step=0.01, format="%.2f")
with col4:
    width_input = st.number_input("5. Width 너비 (mm)", min_value=500.0, max_value=2000.0, value=1200.0, step=1.0)
    st.caption("non-EU 지역은 1200mm 초과/미만 시 보정용으로 사용됩니다.")

st.markdown("---")

# 6. 계산 버튼
if st.button("계산 실행", type="primary"):
    try:
        # 기존 계산 함수 호출
        result = calculate_extra(
            grade=grade_input,
            coating=coating_input,
            thickness=thickness_input,
            width=width_input,
            region=region
        )

        total_usd = result['total_usd_per_mt']
        st.success(f"### 📈 총 EXTRA 비용 (Total Extra): ${total_usd} USD/MT")
        
        # 상세 내역 표시
        st.write("#### 상세 내역")
        breakdown = result['breakdown']
        
        if region == "non-EU":
            st.metric(label="Coating Extra (USD)", value=f"${breakdown['coating_extra_usd']}")
            st.metric(label="Grade Extra (USD)", value=f"${breakdown['grade_extra_usd']}")
            st.metric(label="Width Extra (USD)", value=f"${breakdown['width_extra_usd']}")
        else: # EU
            col_eur1, col_eur2, col_eur3 = st.columns(3)
            with col_eur1:
                st.metric(label="Coating Extra (EUR)", value=f"€{breakdown['coating_extra_eur']}", delta=f"${round(breakdown['coating_extra_eur'] * result['breakdown']['exchange_rate'], 2)} USD")
            with col_eur2:
                st.metric(label="Grade Extra (EUR)", value=f"€{breakdown['grade_extra_eur']}", delta=f"${round(breakdown['grade_extra_eur'] * result['breakdown']['exchange_rate'], 2)} USD")
            with col_eur3:
                st.metric(label="Thick x Width Extra (EUR)", value=f"€{breakdown['thick_width_extra_eur']}", delta=f"${round(breakdown['thick_width_extra_eur'] * result['breakdown']['exchange_rate'], 2)} USD")
            
            st.info(f"**EUR 합계:** €{breakdown['sum_eur']} (환율 1.1082 적용)")

    except Exception as e:
        # 입력값 누락이나 잘못된 형식 처리
        st.error(f"⚠️ 계산 중 오류가 발생했습니다. 입력값을 확인하세요: {e}")

# -----------------------
# Footer
# -----------------------
st.markdown("---")
st.caption("update: 2025.09.29")
st.caption("작성자 : 포스코인터내셔널 태양광강재그룹 구자혁")
