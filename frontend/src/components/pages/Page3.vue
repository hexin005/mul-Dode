<template>
  <div class="page-content">
    <div class="title-container">
      <h2 class="page-title">一方幕布，百种风情</h2>
      <div class="title-decoration"></div>
    </div>
    
    <div class="main-container">
      <!-- 左侧地图区域 -->
      <div class="map-section">
        <div class="map-legend-container">
          <!-- 地图容器 -->
          <div id="mapChart" class="map-container"></div>
          <!-- 图例移动到地图右侧 -->
          <div class="legend-section">
            <div class="map-legend">
              <div v-for="school in schools" :key="school.name" class="map-legend-item">
                <div class="map-legend-color" :style="{ backgroundColor: school.color }"></div>
                <span>{{ school.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 右侧描述区域 -->
      <div class="description-section">
        <h3 class="section-title">皮影戏流派介绍</h3>
        <div class="description-content">
          <p>皮影戏是中国传统民间艺术之一，有着悠久的历史和丰富的文化内涵。根据地域特色和艺术风格，中国皮影戏主要分为七大流派：</p>
<ul>
            <li><strong>秦晋影系</strong>：以陕西为中心，辐射西北各省，风格粗犷豪放。</li>
            <li><strong>滦州影系</strong>：以河北滦州为中心，艺术特点细腻，音乐委婉动听。</li>
            <li><strong>山东影系</strong>：以山东半岛为中心，造型夸张，色彩鲜明。</li>
            <li><strong>杭州影系</strong>：以浙江为中心，风格婉约秀丽，具有江南水乡特色。</li>
            <li><strong>川鄂滇影系</strong>：融合了四川、湖北、云南等地的地方特色，表演生动活泼。</li>
            <li><strong>湘赣影系</strong>：以湖南、江西为中心，音乐和唱腔具有鲜明的地方特色。</li>
            <li><strong>潮州影系</strong>：以粤东、闽南为中心，风格独特，表演技艺精湛。</li>
            <li><strong>特殊说明</strong>：新疆维吾尔自治区：皮影戏由内地移民传入，主要属滦州影系（随东北、华北地区移民）和秦晋影系（随西北开发移民），无独立影系归属。西藏自治区：仅在藏东部分地区有零星分布，受周边省份影响，可归入秦晋影系边缘分布区。安徽省：皖北地区受山东影系影响，皖南地区受杭州影系影响，为两大影系交汇区。</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { schoolData, schools } from '../../asset/data.js'
import chinaMap from '../../asset/china.json'

let chartInstance = null
const router = useRouter()

// 省份到影系和省份代码的映射表
const provinceMap = {
  // 秦晋影系
  '陕西省': { school: 'qinjin', code: 'shaanxi' },
  '甘肃省': { school: 'qinjin', code: 'gansu' },
  '宁夏回族自治区': { school: 'qinjin', code: 'ningxia' },
  '青海省': { school: 'qinjin', code: 'qinghai' },
  '山西省': { school: 'qinjin', code: 'shanxi' },
  
  // 滦州影系
  '河北省': { school: 'luanzhou', code: 'hebei' },
  '北京市': { school: 'luanzhou', code: 'beijing' },
  '天津市': { school: 'luanzhou', code: 'tianjin' },
  '辽宁省': { school: 'luanzhou', code: 'liaoning' },
  '吉林省': { school: 'luanzhou', code: 'jilin' },
  '黑龙江省': { school: 'luanzhou', code: 'heilongjiang' },
  '内蒙古自治区': { school: 'luanzhou', code: 'neimenggu' },
  
  // 山东影系
  '山东省': { school: 'shandong', code: 'shandong' },
  
  // 杭州影系
  '浙江省': { school: 'hangzhou', code: 'zhejiang' },
  '上海市': { school: 'hangzhou', code: 'shanghai' },
  '江苏省': { school: 'hangzhou', code: 'jiangsu' },
  
  // 川鄂滇影系
  '四川省': { school: 'chuanedian', code: 'sichuan' },
  '湖北省': { school: 'chuanedian', code: 'hubei' },
  '河南省': { school: 'chuanedian', code: 'henan' },
  '云南省': { school: 'chuanedian', code: 'yunnan' },
  '贵州省': { school: 'chuanedian', code: 'guizhou' },
  '重庆市': { school: 'chuanedian', code: 'chongqing' },
  
  // 湘赣影系
  '湖南省': { school: 'xianggan', code: 'hunan' },
  '江西省': { school: 'xianggan', code: 'jiangxi' },
  
  // 潮州影系
  '广东省': { school: 'chaozhou', code: 'guangdong' },
  '福建省': { school: 'chaozhou', code: 'fujian' },
  '台湾省': { school: 'chaozhou', code: 'taiwan' },
  '广西壮族自治区': { school: 'chaozhou', code: 'guangxi' },
  '海南省': { school: 'chaozhou', code: 'hainan' },
  '澳门': { school: 'chaozhou', code: 'macau' },
  '香港': { school: 'chaozhou', code: 'hongkong' },
  
  // 其他影系
  '新疆维吾尔自治区': { school: 'other', code: 'xinjiang' },
  '西藏自治区': { school: 'other', code: 'xizang' },
  '安徽省': { school: 'other', code: 'anhui' }
}

// 初始化地图
const initChart = () => {
  try {
    const mapElement = document.getElementById('mapChart')
    if (!mapElement) {
      console.error('地图容器元素未找到')
      return
    }
    
    // 设置地图容器尺寸
    mapElement.style.width = '100%'
    mapElement.style.height = '100%'
    
    chartInstance = echarts.init(mapElement)
    
    // 处理地图数据，移除南海诸岛
    const processedChinaMap = JSON.parse(JSON.stringify(chinaMap))
    processedChinaMap.features = processedChinaMap.features.filter(feature => {
      // 排除南海诸岛
      return feature.properties.name !== '南海诸岛'
    })
    
    echarts.registerMap('china', processedChinaMap)
    
    // 获取地图中所有省份的名称
    const provinceNames = processedChinaMap.features.map(feature => feature.properties.name)
    
    // 创建省份到流派的映射表
    const provinceToSchool = {}
    
    // 秦晋影系 - #FF8A65
    schoolData['秦晋影系'].forEach(province => {
      provinceToSchool[province] = { name: '秦晋影系', color: '#FF8A65', value: 100 }
    })
    
    // 滦州影系 - #4DB6AC
    schoolData['滦州影系'].forEach(province => {
      provinceToSchool[province] = { name: '滦州影系', color: '#4DB6AC', value: 200 }
    })
    
    // 山东影系 - #FFD54F
    schoolData['山东影系'].forEach(province => {
      provinceToSchool[province] = { name: '山东影系', color: '#FFD54F', value: 300 }
    })
    
    // 杭州影系 - #9575CD
    schoolData['杭州影系'].forEach(province => {
      provinceToSchool[province] = { name: '杭州影系', color: '#9575CD', value: 400 }
    })
    
    // 川鄂滇影系 - #66BB6A
    schoolData['川鄂滇影系'].forEach(province => {
      provinceToSchool[province] = { name: '川鄂滇影系', color: '#66BB6A', value: 500 }
    })
    
    // 湘赣影系 - #42A5F5
    schoolData['湘赣影系'].forEach(province => {
      provinceToSchool[province] = { name: '湘赣影系', color: '#42A5F5', value: 600 }
    })
    
    // 潮州影系 - #EC407A
    schoolData['潮州影系'].forEach(province => {
      provinceToSchool[province] = { name: '潮州影系', color: '#EC407A', value: 700 }
    })
    
    // 为所有省份创建数据，移除description字段
    const mapData = provinceNames.map(province => {
      const schoolInfo = provinceToSchool[province]
      if (schoolInfo) {
        return {
          name: province,
          value: schoolInfo.value,
          schoolName: schoolInfo.name,
          itemStyle: { color: schoolInfo.color },
          // 添加省份是否可点击的标记
          clickable: !!provinceMap[province]
        }
      } else {
        // 为未匹配的省份设置默认颜色（浅灰色）
        return {
          name: province,
          value: 0,
          schoolName: '其他影系',
          itemStyle: { color: '#E0E0E0' },
          clickable: !!provinceMap[province]
        }
      }
    })
    
    // 使用visualMap进行颜色映射，同时保留itemStyle.color的优先级
    const option = {
      // 修改tooltip配置，添加点击提示
      tooltip: {
        trigger: 'item',
        formatter: function(params) {
          // 添加点击提示，只有在有映射关系的省份才显示
          const clickTip = provinceMap[params.name] ? 
            '<div style="margin-top: 5px; font-size: 12px; color: #8E24AA;">点击查看详情 →</div>' : '';
            
          return `
            <div style="padding: 10px; border-radius: 6px;">
              <strong style="font-size: 14px; color: #5D4037;">${params.name}</strong><br/>
              <div style="margin-top: 5px;">
                <span style="color: #795548;">流派: </span>
                <span>${params.data.schoolName}</span>
              </div>
              ${clickTip}
            </div>
          `;
        },
        backgroundColor: 'rgba(255, 255, 255, 0.95)',
        borderColor: '#D7CCC8',
        borderWidth: 1,
        borderRadius: 6,
        textStyle: {
          color: '#333',
          fontSize: 13
        },
        transitionDuration: 0.3
      },
      visualMap: {
        show: false,
        min: 0,
        max: 700,
        inRange: {
          color: ['#E0E0E0', '#FF8A65', '#4DB6AC', '#FFD54F', '#9575CD', '#66BB6A', '#42A5F5', '#EC407A']
        }
      },
      series: [{
        name: '皮影戏流派',
        type: 'map',
        map: 'china',
        roam: false,
        // 调整地图缩放和位置，让地图在容器中居中
        zoom: 1.4,
        // 调整中心点，让地图更居中
        center: [105, 37],
        label: {
          show: true,
          fontSize: 12,
          color: '#4E342E',
          fontWeight: 'bold',
          textShadowBlur: 2,
          textShadowColor: 'rgba(255, 255, 255, 0.8)'
        },
        itemStyle: {
          borderColor: '#BDBDBD',
          borderWidth: 0.8,
          areaColor: '#F5F5F5',
          // 设置鼠标指针样式为手型，表明可点击
          cursor: 'pointer'
        },
        // 鼠标悬停效果
        emphasis: {
          itemStyle: {
            shadowBlur: 15,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.3)',
            borderWidth: 1.5
          },
          label: {
            fontSize: 15,
            color: '#212121',
            fontWeight: 'bold',
            textShadowBlur: 3,
            textShadowColor: 'rgba(255, 255, 255, 0.9)'
          },
          emphasisAnimation: true,
          animationDuration: 300
        },
        // 确保每个省份都有数据
        data: mapData,
        // 添加进入动画
        animationDuration: 1000,
        animationEasing: 'cubicOut'
      }]
    }
    
    // 应用配置
    chartInstance.setOption(option, true)
    
    // 添加延迟重新渲染，确保所有省份都正确显示
    setTimeout(() => {
      chartInstance.setOption(option, true)
    }, 100)
    
    // 添加点击事件处理
    chartInstance.on('click', function(params) {
      const provinceInfo = provinceMap[params.name]
      if (provinceInfo) {
        // 构建路由路径，直接跳转到省份详情页
        const routePath = `/school/${provinceInfo.school}/${provinceInfo.code}`
        router.push(routePath)
      }
    })
    
  } catch (error) {
    console.error('地图初始化失败:', error)
  }
}

// 响应式调整
const resizeChart = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

onMounted(() => {
  setTimeout(() => {
    initChart()
  }, 100)
  window.addEventListener('resize', resizeChart)
})

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  window.removeEventListener('resize', resizeChart)
})
</script>

<style scoped>
/* 全局样式重置和基础设置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.page-content {
  width: 100%;
  min-height: 100vh;
  background-color: #FAFAF9;
  background-image: linear-gradient(to bottom, #FAFAF9, #F5F5F0);
  display: flex;
  flex-direction: column;
  padding: 30px;
  font-family: "Noto Serif SC", "SimSun", "宋体", serif;
  color: #424242;
}

/* 标题容器 */
.title-container {
  text-align: center;
  margin-bottom: 40px; 
  position: relative;
  padding-top: 20px;
  z-index: 10; 
}

.page-title {
  font-size: 28px;
  color: #5D4037;
  margin-bottom: 15px;
  font-weight: 700;
  letter-spacing: 2px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.title-decoration {
  width: 80px;
  height: 3px;
  background: linear-gradient(to right, #FF8A65, #FFD54F);
  margin: 0 auto;
  border-radius: 2px;
}

/* 主容器 */
.main-container {
  display: flex;
  flex: 1;
  gap: 30px;
  margin-bottom: 30px;
  min-height: 750px;
}

/* 左侧地图区域 */
.map-section {
  flex: 2;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  min-height: 750px;
  padding: 20px; 
  display: flex;
  flex-direction: column;
}

/* 右侧描述区域 */
.description-section {
  flex: 2; 
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 30px;
  overflow-y: auto;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  min-height: 750px;
}

.map-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
}

/* 地图和图例的容器  */
.map-legend-container {
  display: flex;
  width: 100%;
  height: 100%;
  flex: 1;
}

/* 地图容器 - */
.map-container {
  flex: 1;
  min-height: 650px;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center; 
  justify-content: center; 
}

/* 图例区域  */
.legend-section {
  width: 140px;
  background: rgba(255, 255, 255, 0.95);
  border-left: 1px solid #E0E0E0;
  padding: 20px 15px;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.map-legend {
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: flex-start;
}

.map-legend-item {
  display: flex;
  align-items: center;
  font-size: 12px;
  color: #5D4037;
  white-space: nowrap;
  padding: 5px 8px;
  border-radius: 15px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  width: 100%;
}

.map-legend-item:hover {
  transform: translateX(5px);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.map-legend-color {
  width: 14px;
  height: 14px;
  margin-right: 8px;
  border-radius: 2px;
  border: 1px solid #BDBDBD;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 右侧描述区域 */
.description-section {
  flex: 1;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 30px;
  overflow-y: auto;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  min-height: 750px;
}

.description-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
}

.section-title {
  font-size: 20px;
  color: #5D4037;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #FFE0B2;
  font-weight: 600;
}

.description-content {
  line-height: 1.8;
  color: #555;
  font-size: 15px;
}

.description-content p {
  margin-bottom: 20px;
  text-align: justify;
}

.description-content ul {
  margin-bottom: 20px;
  padding-left: 25px;
}

.description-content li {
  margin-bottom: 12px;
  position: relative;
}

.description-content strong {
  color: #795548;
  font-weight: 600;
}

/* 滚动条样式 */
.description-content::-webkit-scrollbar,
.legend-section::-webkit-scrollbar {
  width: 6px;
}

.description-content::-webkit-scrollbar-track,
.legend-section::-webkit-scrollbar-track {
  background: #F5F5F5;
  border-radius: 3px;
}

.description-content::-webkit-scrollbar-thumb,
.legend-section::-webkit-scrollbar-thumb {
  background: #BDBDBD;
  border-radius: 3px;
}

.description-content::-webkit-scrollbar-thumb:hover,
.legend-section::-webkit-scrollbar-thumb:hover {
  background: #9E9E9E;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-container {
    gap: 20px;
    min-height: 650px;
  }
  
  .map-section,
  .description-section {
    min-height: 650px;
  }
  
  .map-container {
    min-height: 550px;
  }
  
  .legend-section {
    width: 130px;
    padding: 15px 10px;
  }
}

@media (max-width: 1024px) {
  .main-container {
    gap: 15px;
    min-height: 550px;
  }
  
  .map-section,
  .description-section {
    min-height: 550px;
  }
  
  .map-container {
    min-height: 450px;
  }
  
  .legend-section {
    width: 120px;
    padding: 15px 8px;
  }
  
  .map-legend-item {
    font-size: 11px;
    padding: 4px 6px;
  }
}

@media (max-width: 768px) {
  .page-content {
    padding: 20px 15px;
  }
  
  .title-container {
    margin-bottom: 30px;
    padding-top: 10px;
  }
  
  .page-title {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  .main-container {
    flex-direction: column;
    gap: 20px;
    min-height: auto;
  }
  
  .map-section {
    padding: 15px;
  }
  
  .map-section,
  .description-section {
    flex: none;
    width: 100%;
    min-height: 500px;
  }
  
  /* 在移动端将图例移回地图下方 */
  .map-legend-container {
    flex-direction: column;
  }
  
  .legend-section {
    width: 100%;
    height: auto;
    border-left: none;
    border-top: 1px solid #E0E0E0;
    padding: 15px;
  }
  
  .map-legend {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
  }
  
  .map-container {
    min-height: 400px;
  }
  
  .description-section {
    padding: 20px;
  }
  
  .section-title {
    font-size: 18px;
    margin-bottom: 15px;
  }
  
  .description-content {
    font-size: 14px;
  }
}

@media (max-width: 480px) {
  .page-content {
    padding: 15px 10px;
  }
  
  .page-title {
    font-size: 22px;
  }
  
  .map-container {
    min-height: 350px;
  }
  
  .map-legend {
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 5px;
  }
}
</style>