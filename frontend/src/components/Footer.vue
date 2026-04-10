<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3>光影千年-皮影数字化传承</h3>
        <p>专注皮影艺术数字化传承，守护中华非遗瑰宝，让千年影韵走进当代生活。</p>
      </div>
      <div class="footer-section">
        <h3>快速链接</h3>
        <ul>
          <li><a href="/page1">首页</a></li>
          <li><a href="/page2">皮影溯源</a></li>
          <li><a href="/page3">影韵万方</a></li>
          <li><a href="/page4">影魂千年</a></li>
          <li><a href="/page5">匠心工艺</a></li>
        </ul>
      </div>
      <div class="footer-section">
        <h3>联系方式</h3>
        <p>邮箱: 343998@qq.com</p>
        <p>电话: 19962206256</p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 光影千年-皮影数字化传承. 版权所有 </p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background: linear-gradient(to right, #0a3d31, #1a5e4d, #0a3d31);
  color: #f0f0f0;
  padding: 30px 0 10px;
  width: 100%;
  box-sizing: border-box;
  flex-shrink: 0;
  position: relative;
  z-index: 1000;
  margin-top: auto;
  clear: both;
  bottom: 0;
}


.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  padding: 0 20px;
  gap: 20px;
}

.footer-section {
  flex: 1;
  min-width: 250px;
  padding: 10px;
}

.footer-section h3 {
  color: #d4fc79;
  margin-bottom: 15px;
  font-size: 1.2em;
  border-bottom: 1px solid #d4fc79;
  padding-bottom: 5px;
}

.footer-section ul {
  list-style: none;
  padding: 0;
}

.footer-section ul li {
  margin-bottom: 8px;
}

.footer-section ul li a {
  color: #f0f0f0;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-section ul li a:hover {
  color: #d4fc79;
  text-decoration: underline;
}

.footer-section p {
  line-height: 1.6;
  margin-bottom: 10px;
}

.footer-bottom {
  max-width: 1200px;
  margin: 20px auto 0;
  padding: 15px 20px 0;
  text-align: center;
  border-top: 1px solid rgba(212, 252, 121, 0.2);
}

.footer-bottom p {
  margin: 0;
  font-size: 0.9em;
  color: #ccc;
}

.footer-bottom a {
  color: #d4fc79;
  text-decoration: none;
  margin: 0 10px;
}

.footer-bottom a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .footer-content {
    flex-direction: column;
    text-align: center;
  }
  
  .footer-section {
    min-width: auto;
  }
}
</style>