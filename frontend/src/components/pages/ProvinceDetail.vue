<template>
    <div class="province-detail-container">
        <!-- 顶部区域：返回按钮 + 影系名称 -->
        <div class="top-section">
            <!-- 返回按钮 -->
            <div class="back-button" @click="goBack">
                ← 返回
            </div>
            <!-- 影系名称 -->
            <h1 class="school-name">{{ provinceData ? provinceData.school_name : '' }}</h1>
        </div>

        <!-- 省份详情内容 -->
        <div v-if="provinceData && !loading" class="main-content">
            <!-- 左侧省份导航 -->
            <div class="province-nav">
                <div class="province-list">
                    <div v-for="province in filteredProvinces" :key="province.id" class="province-item"
                        :class="{ active: province.id === provinceData.id }" @click="selectProvince(province)">
                        {{ province.province_name }}
                    </div>
                </div>
            </div>

            <!-- 右侧内容区域 -->
            <div class="content-wrapper">
                <!-- 中间6张图片展示 -->
                <div class="images-section">
                    <div class="show">
                        <div class="slide">
                            <div v-for="i in 6" :key="i" class="slide-item" :class="`item${i-1}`">
                                <img v-if="provinceData[`image${i}`]" :src="getImagePath(provinceData[`image${i}`], i)"
                                    :alt="`图${i}`" @error="handleImageError" />
                                <div v-else class="image-placeholder">图{{ i }}</div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="description-section">
                    <dl>
                        <dt><b>流行地区</b>：{{ provinceData.region || '暂无信息' }}</dt>
                        <dt><b>艺术特色</b>：</dt>
                        <dd>造型：{{ provinceData.shape_features || '暂无信息' }}</dd>
                        <dd>色彩：{{ provinceData.color_features || '暂无信息' }}</dd>
                        <dd>唱腔：{{ provinceData.singing_features || '暂无信息' }}</dd>
                        <dt><b>代表剧目</b>：{{ provinceData.representative_plays || '暂无信息' }}</dt>
                    </dl>
                </div>
            </div>
            <!-- 加载状态 -->
            <div v-if="loading" class="loading">
                数据加载中...
            </div>

            <!-- 错误状态 -->
            <div v-if="error && !loading" class="error">
                {{ error }}
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'ProvinceDetail',
  data() {
    return {
      provinceData: null,
      loading: true,
      error: null,
      allProvinces: [],
      selectedProvinceId: null
    };
  },
  computed: {
    currentSchoolName() {
      return this.provinceData ? this.provinceData.school_name : '';
    },
    filteredProvinces() {
      if (!this.allProvinces.length || !this.currentSchoolName) {
        return [];
      }
      return this.allProvinces.filter(province => province.school_name === this.currentSchoolName);
    }
  },
  async mounted() {
    await this.fetchAllProvinces();
    await this.fetchProvinceDetail();
  },
  methods: {
    async fetchAllProvinces() {
      try {
        this.allProvinces = await this.$api.getProvinces();
      } catch (err) {
        console.error('获取所有省份失败:', err);
      }
    },
    async fetchProvinceDetail() {
      this.loading = true;
      this.error = null;
      
      try {
        // 从路由参数获取省份ID
        const provinceId = this.$route.params.id;
        if (provinceId) {
          // 如果有ID参数，按原来的方式获取数据
          const data = await this.$api.getProvinceDetail(provinceId);
          this.provinceData = data;
        } else {
          // 新的路由方式：根据影系和省份名称获取数据
          const schoolName = this.$route.params.schoolName;
          const provinceName = this.$route.params.provinceName;
          
          if (!schoolName || !provinceName) {
            throw new Error('未指定影系或省份');
          }
          
          // 使用新的API方法获取数据
          const data = await this.$api.getProvinceBySchoolAndName(schoolName, provinceName);
          this.provinceData = data;
        }
      } catch (err) {
        console.error('获取省份详情失败:', err);
        this.error = '获取省份详情失败，请稍后重试';
      } finally {
        this.loading = false;
      }
    },
    selectProvince(province) {
      // 修复路由路径，应该使用 /school/ 而不是 /province/
      this.$router.push(`/school/${province.school_name}/${province.province_name}`);
      // 更新当前选中的省份数据
      this.provinceData = province;
    },
    getImagePath(imageValue, index) {
      // 处理各种可能的图片路径情况
      if (!imageValue) return '';
      
      // 如果已经是完整URL，直接返回
      if (imageValue.startsWith('http')) {
        return imageValue;
      }
      
      // 如果路径是 images/map/ 开头的完整路径格式，直接使用
      if (imageValue.startsWith('images/map/') && imageValue.includes('(')) {
        return `http://localhost:5000/${imageValue}`;
      }
      
      // 如果是只有省份代码的格式（如 "hnpy"），构造完整路径
      if (!imageValue.includes('/') && !imageValue.includes('.')) {
        // 根据数据库中实际的文件命名规则构造路径
        // 文件命名格式为 {省份代码}py ({序号}).{扩展名}
        return `http://localhost:5000/images/map/${imageValue} (${index}).png`;
      }
      
      // 其他情况，尝试直接使用
      return `http://localhost:5000/images/map/${imageValue}`;
    },
    handleImageError(event) {
      // 图片加载失败时的处理
      console.warn('图片加载失败:', event.target.src);
      // 可以设置默认图片或其他处理
      event.target.style.display = 'none';
    },
    goBack() {
      // 修复返回逻辑，明确返回到page3页面
      this.$router.push('/page3');
    }
  }
};
</script>

<style scoped>
/* 导入中文字体 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&family=Ma+Shan+Zheng&display=swap');
@import '../../asset/show.css';

.province-detail-container {
  padding: 0;
  max-width: none;
  margin: 0;
  font-family: "Noto Serif SC", "SimSun", "宋体", serif;
  background: linear-gradient(135deg, #f9f3e9 0%, #faf6f0 100%);
  min-height: 100vh;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 确保整个页面没有滚动条 */
}

.province-detail-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('../../asset/img/opacity-b25.png') repeat;
  opacity: 0.1;
  z-index: 0;
}

/* 顶部区域样式 */
.top-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px 30px;
  border-bottom: 2px solid #D7CCC8;
  position: relative;
  z-index: 1;
  flex-shrink: 0;
}

.back-button {
  cursor: pointer;
  color: #8B4513;
  font-size: 18px;
  display: inline-block;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.back-button:hover {
  color: #5D4037;
  background: rgba(255, 255, 255, 0.9);
  transform: translateX(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.school-name {
  font-size: 2.5rem;
  color: #5D4037;
  margin: 0;
  font-weight: 700;
  font-family: 'Ma Shan Zheng', cursive;
  letter-spacing: 2px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  flex: 1;
  text-align: center;
  padding: 5px 0;
}

/* 主内容区域 - 左右分栏布局 */
.main-content {
  display: flex;
  flex: 1;
  gap: 20px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  overflow: hidden;
  position: relative;
  z-index: 1;
  margin: 0;
  width: 100%;
  padding: 20px;
  box-sizing: border-box;
}

/* 左侧省份导航 */
.province-nav {
  width: 220px;
  background: linear-gradient(160deg, #f8f4ee 0%, #fdfaf5 100%);
  padding: 15px 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  height: calc(100vh - 160px);
  margin: 0;
  border: none;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}

.province-list {
  height: 100%;
  overflow-y: auto;
  padding-right: 5px;
}

.province-list::-webkit-scrollbar {
  width: 6px;
}

.province-list::-webkit-scrollbar-track {
  background: rgba(215, 204, 200, 0.2);
  border-radius: 3px;
}

.province-list::-webkit-scrollbar-thumb {
  background: #D7CCC8;
  border-radius: 3px;
}

.province-item {
  padding: 12px 15px;
  margin-bottom: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #616161;
  font-weight: 500;
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(215, 204, 200, 0.3);
  font-size: 0.95rem;
}

.province-item::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: #D7CCC8;
  transform: scaleY(0);
  transition: transform 0.3s ease;
}

.province-item:hover {
  background: rgba(255, 255, 255, 0.95);
  color: #5D4037;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.province-item:hover::before {
  transform: scaleY(1);
}

.province-item.active {
  background: linear-gradient(90deg, #8B4513 0%, #A0522D 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(139, 69, 19, 0.3);
  border: 1px solid rgba(139, 69, 19, 0.5);
}

.province-item.active::before {
  background: #FFD54F;
}

/* 右侧内容区域 */
.content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  overflow: hidden;
  padding-right: 0px; /* 向右偏移 */
}

/* 图片展示区域样式 */
.images-section {
  flex: 1;
  min-height: 0;
}

.show {
  height: 100%;
  align-items: center;
  text-align: center;
  padding-top: 0;
  margin-left: 50px; /* 调整回更合适的位置 */
  width: 90%;
}
.slide {
  width: 100%;
  height: 100%;
  perspective: preserve-3d;
}

.slide .slide-item {
  position: absolute;
  height: 100%;
  -webkit-transform-origin: top left;
  -ms-transform-origin: top left;
  transform-origin: top left;
  -webkit-transition: all ease .8s;
  transition: all ease .8s;
}

.slide img {
  display: block;
  position: relative;
  width: auto;
  height: 60%; /* 进一步缩小图片高度 */
  max-height: none;
  object-fit: contain;
  border-radius: 10px;
  margin: 0 auto; /* 居中显示 */
}

.image-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 60%; /* 与图片高度一致 */
  background: linear-gradient(135deg, #f0e6d2 0%, #f5f0e6 100%);
  border: 1px dashed #D7CCC8;
  border-radius: 10px;
  color: #A1887F;
  font-size: 1.3rem;
  font-weight: 500;
  margin: 0 auto; /* 居中显示 */
}

/* 描述部分样式 - 修改为完全显示，无滚动条 */
.description-section {
  background: linear-gradient(135deg, #f8f4ee 0%, #fdfaf5 100%);
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  position: relative;
  overflow: hidden; /* 隐藏溢出内容 */
  border: 1px solid rgba(220, 190, 150, 0.3);
  transition: all 0.3s ease;
  padding: 20px;
  flex-shrink: 0;
  max-height: none; /* 移除最大高度限制 */
}

.description-section:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}

.description-section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #8B4513, #D7CCC8);
}

.description-section dl {
  margin: 0;
  line-height: 1.6;
  max-height: none; /* 移除最大高度限制 */
  overflow-y: hidden; /* 隐藏垂直滚动条 */
}

.description-section dt {
  font-weight: 600;
  color: #5D4037;
  margin-bottom: 10px;
  font-size: 1.1rem;
  border-bottom: 1px solid #D7CCC8;
  padding-bottom: 8px;
}

.description-section dd {
  margin-left: 15px;
  margin-bottom: 8px;
  color: #616161;
  font-size: 1rem;
}

/* 加载和错误状态 */
.loading,
.error {
  text-align: center;
  font-size: 1.3rem;
  padding: 30px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  margin: auto;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loading {
  color: #8B4513;
}

.error {
  color: #e74c3c;
  background: rgba(255, 255, 255, 0.9);
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .province-detail-container {
    padding: 0;
  }
  
  .main-content {
    flex-direction: column;
    padding: 15px;
  }
  
  .province-nav {
    width: 100%;
    height: auto;
    max-height: 200px;
    margin: 0;
  }
  
  .province-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    max-height: 180px;
  }
  
  .province-item {
    flex: 1 1 calc(33.333% - 10px);
    margin-bottom: 0;
    text-align: center;
  }
  
  .content-wrapper {
    padding: 0;
  }
  
  .school-name {
    font-size: 2rem;
  }
  
  .show {
    height: 60vh;
    margin-left: 0;
    width: 100%;
  }
  
  .slide img {
    height: 50%; /* 在中等屏幕上进一步调整图片高度 */
  }
  
  .image-placeholder {
    height: 50%; /* 与图片高度一致 */
  }
  
  .description-section {
    max-height: none;
  }
  
  .description-section dl {
    max-height: none;
    overflow-y: hidden; /* 隐藏垂直滚动条 */
  }
}

@media (max-width: 768px) {
  .province-detail-container {
    padding: 0;
  }
  
  .top-section {
    padding: 10px 20px;
  }
  
  .back-button {
    font-size: 16px;
    padding: 6px 12px;
  }
  
  .main-content {
    gap: 15px;
    padding: 10px;
  }
  
  .province-nav {
    padding: 10px;
    max-height: 150px;
  }
  
  .province-list {
    max-height: 130px;
    gap: 5px;
  }
  
  .province-item {
    flex: 1 1 calc(50% - 5px);
    padding: 8px 10px;
    font-size: 0.9rem;
  }
  
  .school-name {
    font-size: 1.6rem;
  }
  
  .description-section {
    padding: 15px;
  }
  
  .description-section dt {
    font-size: 1rem;
  }
  
  .description-section dd {
    font-size: 0.9rem;
    margin-left: 10px;
  }
  
  .show {
    height: 50vh;
  }
  
  .slide img {
    height: 40%; /* 在小屏幕上进一步调整图片高度 */
  }
  
  .image-placeholder {
    height: 40%; /* 与图片高度一致 */
  }
}

@media (max-width: 480px) {
  .province-detail-container {
    padding: 0;
  }
  
  .top-section {
    padding: 8px 15px;
  }
  
  .back-button {
    font-size: 14px;
    padding: 5px 10px;
  }
  
  .school-name {
    font-size: 1.4rem;
  }
  
  .main-content {
    gap: 10px;
    padding: 8px;
  }
  
  .province-nav {
    padding: 8px;
    max-height: 120px;
  }
  
  .province-list {
    max-height: 100px;
    gap: 4px;
  }
  
  .province-item {
    flex: 1 1 calc(50% - 4px);
    padding: 6px 8px;
    font-size: 0.8rem;
  }
  
  .description-section {
    padding: 12px;
  }
  
  .description-section dt {
    font-size: 0.9rem;
  }
  
  .description-section dd {
    font-size: 0.8rem;
    margin-left: 8px;
  }
  
  .show {
    height: 40vh;
  }
  
  .slide img {
    height: 30%; /* 在小屏幕上进一步调整图片高度 */
  }
  
  .image-placeholder {
    height: 30%; /* 与图片高度一致 */
  }
}
</style>