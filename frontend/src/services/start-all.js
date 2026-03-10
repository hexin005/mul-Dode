import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

// 获取当前文件的目录路径
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 启动后端服务
function startBackend() {
    console.log('\n🚀 正在启动后端服务...');
    const backendProcess = spawn('python', ['app.py'], {
        cwd: join(__dirname, '../../backend'),
        shell: true,
        stdio: 'inherit'
    });

    backendProcess.on('error', (error) => {
        console.error('❌ 启动后端服务失败:', error.message);
        process.exit(1);
    });

    backendProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`❌ 后端服务异常退出，退出码: ${code}`);
        }
    });

    return backendProcess;
}

// 启动前端服务
function startFrontend() {
    console.log('🚀 正在启动前端服务...');
    const frontendProcess = spawn('npm', ['run', 'dev'], {
        cwd: join(__dirname, '../../'),
        shell: true,
        stdio: 'inherit'
    });

    frontendProcess.on('error', (error) => {
        console.error('❌ 启动前端服务失败:', error.message);
        process.exit(1);
    });

    frontendProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`❌ 前端服务异常退出，退出码: ${code}`);
        }
    });

    return frontendProcess;
}

// 主函数
function main() {
    console.log('====================================');
    console.log('🎭 正在启动皮影艺术展示系统...');
    console.log('====================================');
    
    // 先启动后端
    const backend = startBackend();
    
    // 延迟3秒启动前端，确保后端服务已经运行
    setTimeout(() => {
        const frontend = startFrontend();
        
        // 延迟2秒后显示访问提示
        setTimeout(() => {
            console.log('\n====================================');
            console.log('🎉 所有服务已成功启动！');
            console.log('====================================');
            console.log('🌐 前端访问地址: http://localhost:5173');
            console.log('🔧 后端API地址: http://localhost:5000/api');
            console.log('====================================');
            console.log('💡 提示: 按 Ctrl+C 可以同时关闭所有服务');
            console.log('====================================');
            console.log('ℹ️  请手动访问 http://localhost:5173 以打开前端页面');
        }, 2000);
        
        // 监听终端退出信号，确保子进程也能正确关闭
        process.on('SIGINT', () => {
            console.log('\n====================================');
            console.log('⏹️  正在关闭所有服务...');
            console.log('====================================');
            backend.kill();
            frontend.kill();
            process.exit(0);
        });
    }, 3000);
}

// 启动服务
main();