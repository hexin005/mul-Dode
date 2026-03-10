// API服务模块
const API_BASE_URL = 'http://localhost:5000/api';

// 获取所有省份信息
export const getProvinces = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/provinces/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('获取省份信息失败:', error);
    throw error;
  }
};

// 根据ID获取省份详情
export const getProvinceDetail = async (provinceId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/provinces/${provinceId}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('获取省份详情失败:', error);
    throw error;
  }
};

// 获取所有影系信息
export const getSchools = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/schools/`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  } catch (error) {
    console.error('获取影系信息失败:', error);
    throw error;
  }
};

// 根据影系和省份名称获取省份详情
export const getProvinceBySchoolAndName = async (schoolName, provinceName) => {
  try {
    // 获取所有省份数据
    const provinces = await getProvinces();
    
    // 查找匹配的省份数据
    const matchedProvince = provinces.find(province => {
      // 将中文影系名称转换为拼音进行比较
      const schoolNameMap = {
        'qinjin': '秦晋影系',
        'luanzhou': '滦州影系',
        'shandong': '山东影系',
        'hangzhou': '杭州影系',
        'chuanedian': '川鄂滇影系',
        'xianggan': '湘赣影系',
        'chaozhou': '潮州影系',
        'other': '其他影系'
      };
      
      // 省份名称映射
      const provinceNameMap = {
        'gansu': '甘肃省',
        'shaanxi': '陕西省',
        'ningxia': '宁夏回族自治区',
        'qinghai': '青海省',
        'shanxi': '山西省',
        'hebei': '河北省',
        'beijing': '北京市',
        'tianjin': '天津市',
        'liaoning': '辽宁省',
        'jilin': '吉林省',
        'heilongjiang': '黑龙江省',
        'neimenggu': '内蒙古自治区',
        'shandong': '山东省',
        'zhejiang': '浙江省',
        'shanghai': '上海市',
        'jiangsu': '江苏省',
        'sichuan': '四川省',
        'hubei': '湖北省',
        'henan': '河南省',
        'yunnan': '云南省',
        'guizhou': '贵州省',
        'chongqing': '重庆市',
        'hunan': '湖南省',
        'jiangxi': '江西省',
        'guangdong': '广东省',
        'fujian': '福建省',
        'taiwan': '台湾省',
        'guangxi': '广西壮族自治区',
        'hainan': '海南省',
        'macau': '澳门特别行政区',
        'hongkong': '香港特别行政区',
        'xinjiang': '新疆维吾尔自治区',
        'xizang': '西藏自治区',
        'anhui': '安徽省'
      };
      
      const chineseSchoolName = schoolNameMap[schoolName] || schoolName;
      const chineseProvinceName = provinceNameMap[provinceName] || provinceName;
      
      return province.school_name === chineseSchoolName && 
             province.province_name === chineseProvinceName;
    });
    
    if (matchedProvince) {
      return matchedProvince;
    } else {
      throw new Error('未找到匹配的省份数据');
    }
  } catch (error) {
    console.error('获取省份详情失败:', error);
    throw error;
  }
};