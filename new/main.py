import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.interpolate import CubicSpline

# Ruta al CSV descargado de Investing.com
csv_path = 'TSLA_historical.csv'

# 1. Cargar y limpiar datos
df = pd.read_csv(
    csv_path,
    header=0,
    sep=',',
    parse_dates=['Fecha'],
    dayfirst=True
)
df.rename(columns={'Último': 'Price'}, inplace=True)
df['Price'] = (
    df['Price']
      .str.replace('.', '', regex=False)
      .str.replace(',', '.', regex=False)
      .astype(float)
)
df.sort_values('Fecha', inplace=True)
df.set_index('Fecha', inplace=True)

# 2. Construir spline cúbico
x = mdates.date2num(df.index.to_pydatetime())
cs = CubicSpline(x, df['Price'].values)

# 3. Definir eventos y variaciones reales
events = {
    'FSD Beta': ('2023-02-15', -1.5),
    'Cybertruck vid. rota': ('2019-11-22', -6.0),
    'Accidente Autopilot': ('2021-04-18', -3.4),
    'Investigación NHTSA': ('2021-08-16', -4.0),
}

# 4. Proyección 2019–2025 y línea de tiempo
start = pd.to_datetime('2019-01-01')
end   = pd.to_datetime('2025-05-20')
proj_df = df.loc[start:end]

fig, ax = plt.subplots(figsize=(12, 5))

# Línea principal en verde
ax.plot(proj_df.index, proj_df['Price'], color='green', linewidth=2, label='TSLA Precio de cierre')

# Marcar cada evento
for label, (date_str, pct) in events.items():
    fecha_dt = pd.to_datetime(date_str)
    precio_evt = cs(mdates.date2num(fecha_dt))
    ax.scatter([fecha_dt], [precio_evt], color='red', zorder=5)
    ax.text(
        fecha_dt, precio_evt,
        f"{pct:.1f}%",
        color='red',
        rotation=0,
        va='bottom',
        ha='center',
        backgroundcolor='white'
    )

# Formato del eje x: ticks anuales
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

ax.set_title('Línea de tiempo de TSLA (2019–2025) con escándalos y % de variación', pad=15)
ax.set_xlabel('Año')
ax.set_ylabel('Precio de cierre (USD)')
ax.grid(True, linestyle='--', alpha=0.5)
ax.legend()

plt.tight_layout()
# Guardar figura localmente
plt.savefig('Timeline_TSLA_2019-2025.png', dpi=300)
plt.show()
