from shapely.geometry import LineString
import math
from shapely.geometry import Point, Polygon, shape
import mapclassify
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
import time  # 导入time库，时间戳
import numpy as np
import pandas as pd
import warnings  # 运行这个代码可以让Python不显示warnings
warnings.filterwarnings("ignore")
df = pd.read_csv('test.txt', header=None)
#给数据命名列, '车号','时间','经度','纬度','空车（1为载客，0为空车）','速度'
df.columns = ['VehicleNum', 'Stime', 'Lng', 'Lat', 'OpenStatus', 'Speed']
# print(df.head(10))#查看前10条数据

df = df.sort_values(by=['VehicleNum', 'Stime'])  # 根据车牌号和时间进行排序

# 排序之后一段OD轨迹应为都是0或都是1，但数据中有可能出现前后都是0，突然有一条数据变成1，
# 或者前后都是1，突然变成0。这种异常情况我们是要排除的
df = df[-((df['OpenStatus'].shift() == df['OpenStatus'].shift(-1)) &
          (df['OpenStatus'].shift(-1) != df['OpenStatus']) &
          (df['VehicleNum'].shift(-1) == df['VehicleNum']) &
          (df['VehicleNum'].shift() == df['VehicleNum']))]

lon1 = 113.75194
lon2 = 114.624187
lat1 = 22.447837
lat2 = 22.864748
df_sz = df[(df['Lng'] >= lon1) &
           (df['Lng'] <= lon2) &
           (df['Lat'] >= lat1) &
           (df['Lat'] <= lat2)]

df_sz['OpenStatus1'] = df_sz['OpenStatus'].shift(-1)
# 创建一列StatusChange，它的值是OpenStatus1减去OpenStatus，表示载客状态的变化
df_sz['StatusChange'] = df_sz['OpenStatus1']-df_sz['OpenStatus']
# 提取其中的OD信息
oddata = df_sz[(df_sz['StatusChange'] == 1) | (df_sz['StatusChange'] == -1) &
               (df_sz['VehicleNum'] == df_sz['VehicleNum'].shift(-1))]
oddata = oddata[['VehicleNum', 'Stime', 'Lng', 'Lat', 'StatusChange']]
oddata.columns = ['VehicleNum', 'Stime', 'SLng', 'SLat', 'StatusChange']
oddata['Etime'] = oddata['Stime'].shift(-1)
oddata['ELng'] = oddata['SLng'].shift(-1)
oddata['ELat'] = oddata['SLat'].shift(-1)
oddata = oddata[(oddata['VehicleNum'] == oddata['VehicleNum'].shift(-1)) &
                (oddata['StatusChange'] == 1)]
oddata = oddata.drop('StatusChange', axis=1)
#print(oddata.head())

sz = gpd.GeoDataFrame.from_file(
    '深圳市.json', encoding='utf-8')
sz.plot()
#plt.show()

#定义一个测试栅格划的经纬度
testlon = 114
testlat = 22.5

#划定栅格划分范围
lon1 = 113.75194
lon2 = 114.624187
lat1 = 22.447837
lat2 = 22.864748

latStart = min(lat1, lat2)
lonStart = min(lon1, lon2)

#定义栅格大小(单位m)
accuracy = 500

#计算栅格的经纬度增加量大小Lon和Lat
deltaLon = accuracy * 360 / \
    (2 * math.pi * 6371004 * math.cos((lat1 + lat2) * math.pi / 360))
deltaLat = accuracy * 360 / (2 * math.pi * 6371004)

#计算栅格的经纬度编号
LONCOL = divmod(float(testlon) - (lonStart - deltaLon / 2), deltaLon)[0]
LATCOL = divmod(float(testlat) - (latStart - deltaLat / 2), deltaLat)[0]

#计算栅格的中心点经纬度
#HBLON = LONCOL*deltaLon + (lonStart - deltaLon / 2)#格子编号*格子宽+起始横坐标-半个格子宽=格子中心横坐标
#HBLAT = LATCOL*deltaLat + (latStart - deltaLat / 2)
#以下为更正，不需要减去半个格子宽
HBLON = LONCOL*deltaLon + lonStart  # 格子编号*格子宽+起始横坐标=格子中心横坐标
HBLAT = LATCOL*deltaLat + latStart


#定义空的geopandas表
data = gpd.GeoDataFrame()

#定义空的list，后面循环一次就往里面加东西
LONCOL = []
LATCOL = []
geometry = []
HBLON1 = []
HBLAT1 = []

#计算总共要生成多少个栅格
#lon方向是lonsnum个栅格
lonsnum = int((lon2-lon1)/deltaLon)+1
#lat方向是latsnum个栅格
latsnum = int((lat2-lat1)/deltaLat)+1

for i in range(lonsnum):
    for j in range(latsnum):

        HBLON = i*deltaLon + lonStart
        HBLAT = j*deltaLat + latStart
        #把生成的数据都加入到前面定义的空list里面
        LONCOL.append(i)
        LATCOL.append(j)
        HBLON1.append(HBLON)
        HBLAT1.append(HBLAT)

        #生成栅格的Polygon形状
        HBLON_1 = (i+1)*deltaLon + lonStart
        HBLAT_1 = (j+1)*deltaLat + latStart
        geometry.append(Polygon([
            (HBLON-deltaLon/2, HBLAT-deltaLat/2),
            (HBLON_1-deltaLon/2, HBLAT-deltaLat/2),
            (HBLON_1-deltaLon/2, HBLAT_1-deltaLat/2),
            (HBLON-deltaLon/2, HBLAT_1-deltaLat/2)]))

#为geopandas文件的每一列赋值为刚刚的list
data['LONCOL'] = LONCOL
data['LATCOL'] = LATCOL
data['HBLON'] = HBLON1
data['HBLAT'] = HBLAT1
data['geometry'] = geometry

#筛选出深圳范围的栅格
grid_sz = data[data.intersects(sz.unary_union)]
grid_sz.plot()
#plt.show()

oddata = oddata[-oddata['Etime'].isnull()]
oddata['SLONCOL'] = (
    (oddata['SLng']-(lonStart - deltaLon / 2))/deltaLon).astype('int')
oddata['SLATCOL'] = (
    (oddata['SLat']-(latStart - deltaLat / 2))/deltaLat).astype('int')
oddata['ELONCOL'] = (
    (oddata['ELng']-(lonStart - deltaLon / 2))/deltaLon).astype('int')
oddata['ELATCOL'] = (
    (oddata['ELat']-(latStart - deltaLat / 2))/deltaLat).astype('int')
#集计
oddata = oddata.groupby(['SLONCOL', 'SLATCOL', 'ELONCOL', 'ELATCOL'])[
    'VehicleNum'].count().rename('count').reset_index()

#筛选范围内的栅格
oddata = oddata[(oddata['SLONCOL'] >= 0) & (oddata['SLONCOL'] <= lonsnum) &
                (oddata['SLATCOL'] >= 0) & (oddata['SLATCOL'] <= latsnum) &
                (oddata['ELONCOL'] >= 0) & (oddata['ELONCOL'] <= lonsnum) &
                (oddata['ELATCOL'] >= 0) & (oddata['ELATCOL'] <= latsnum)]
#计算栅格的中心点经纬度
oddata['SHBLON'] = oddata['SLONCOL'] * \
    deltaLon + lonStart  # 格子编号*格子宽+起始横坐标=格子中心横坐标
oddata['SHBLAT'] = oddata['SLATCOL']*deltaLat + latStart
oddata['EHBLON'] = oddata['ELONCOL'] * \
    deltaLon + lonStart  # 格子编号*格子宽+起始横坐标=格子中心横坐标
oddata['EHBLAT'] = oddata['ELATCOL']*deltaLat + latStart

oddata = gpd.GeoDataFrame(oddata)
r = oddata.iloc[0]
oddata['geometry'] = oddata.apply(lambda r: LineString(
    [[r['SHBLON'], r['SHBLAT']], [r['EHBLON'], r['EHBLAT']]]), axis=1)
oddata.plot()
#plt.show()

fig = plt.figure(1, (16, 8), dpi=300)
ax = plt.subplot(111)
plt.sca(ax)

#绘制栅格
grid_sz.plot(ax=ax, edgecolor=(0, 0, 0, 0.8),
             facecolor=(0, 0, 0, 0), linewidths=0.02)

#绘制深圳的边界
sz_all = gpd.GeoDataFrame()
sz_all['geometry'] = [sz.unary_union]
sz_all.plot(ax=ax, edgecolor=(0, 0, 0, 1),
            facecolor=(0, 0, 0, 0), linewidths=0.5)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
plt.title('深圳市出租车OD分布', fontsize=18, verticalalignment='center',
          horizontalalignment='center')
#设置colormap的数据
vmax = oddata['count'].max()
cmapname = 'cool'
cmap = mpl.cm.get_cmap(cmapname)

#绘制OD
oddata.plot(ax=ax, column='count', linewidth=15 *
            (oddata['count']/oddata['count'].max()), cmap=cmap, vmin=0, vmax=vmax, alpha=0.4)

plt.axis('off')
#设定显示范围
ax.set_xlim(113.6, 114.8)
ax.set_ylim(22.4, 22.9)

#绘制colorbar
plt.imshow([[0, vmax]], cmap=cmap)
cax = plt.axes([0.08, 0.4, 0.02, 0.3])
plt.colorbar(cax=cax)

#保存图片
##plt.savefig(r'深圳市出租车OD分布.jpg',dpi=300)
#显示图
plt.show()

