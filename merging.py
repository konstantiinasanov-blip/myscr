import pandas as pd
import re
def get_eight_digits(order_id):
    nums = re.findall(r'\d+', str(order_id))
    if nums:
        return nums[0][:8]
    return None
df_1c = pd.read_excel('1C.xlsx', dtype=str)
df_wms = pd.read_excel('WMS.xlsx', dtype=str)
df_1c['ключ'] = df_1c.iloc[:, 0].apply(get_eight_digits)
df_wms['ключ'] = df_wms.iloc[:, 0].apply(get_eight_digits)
merged = pd.merge(
    df_1c,
    df_wms,
    on='ключ',
    how='left',
    suffixes=('_1c', '_wms')
)
merged['№'] = range(1, len(merged) + 1)
raw_date = merged.iloc[:, 1]
merged['Дата документа'] = pd.to_datetime(raw_date, errors='coerce').dt.strftime('%d.%m.%Y')
merged['Номер документа'] = merged.iloc[:, 0]
merged['Вид документа'] = 'Реализация товаров и услуг'
status_col = None
if 'Статус_wms' in merged.columns:
    status_col = 'Статус_wms'
elif 'Статус' in merged.columns:
    status_col = 'Статус'

if status_col:
    merged['WMS'] = merged[status_col].fillna('Нет в WMS')
    def get_1c_status(row):
        if pd.isna(row[status_col]):
            return ''
        if row[status_col] == 'Хост':
            return 'Проведен'
        elif row[status_col] in ['Нач.', 'Созд.']:
            return 'Не проведен'
        return ''
    
    merged['1C'] = merged.apply(get_1c_status, axis=1)
else:
    merged['WMS'] = 'Нет в WMS'
    merged['1C'] = ''
vid_col = None
if 'Вид заказа_wms' in merged.columns:
    vid_col = 'Вид заказа_wms'
elif 'Вид заказа' in merged.columns:
    vid_col = 'Вид заказа'

if vid_col:
    merged['Вид'] = merged[vid_col].fillna('')
else:
    merged['Вид'] = ''
result = merged[[
    '№',
    'Дата документа',
    'Номер документа',
    'Вид документа',
    'WMS',
    '1C',
    'Вид'
]]
result.to_excel('result.xlsx', index=False)
input("\nГотово! Нажми Enter, чтобы выйти...")