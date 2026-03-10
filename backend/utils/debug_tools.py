import requests
import json
import time
import traceback

def debug_image_generation():
    # API端点
    endpoint = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
    
    # 请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer ebc60465-6a32-49d6-9afd-40da7c4b9f1c"
    }
    
    # 请求数据
    payload = {
        "model": "doubao-seedream-4-0-250828",
        "prompt": "星际穿越，黑洞，黑洞里冲出一辆快支离破碎的复古列车，抢视觉冲击力，电影大片，末日既视感，动感，对比色，oc渲染，光线追踪，动态模糊，景深，超现实主义，深蓝，画面通过细腻的丰富的色彩层次塑造主体与场景，质感真实，暗黑风背景的光影效果营造出氛围，整体兼具艺术幻想感，夸张的广角透视效果，耀光，反射，极致的光影，强引力，吞噬",
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": "2K",
        "stream": False,
        "watermark": True
    }
    
    try:
        print("===== 开始调试图像生成API =====")
        print(f"请求URL: {endpoint}")
        print(f"请求模型: {payload['model']}")
        print(f"请求头(不含密钥): Content-Type={headers['Content-Type']}")
        print(f"请求大小: 约{len(json.dumps(payload))} 字符")
        
        start_time = time.time()
        print(f"开始发送请求... ({time.strftime('%H:%M:%S')})")
        
        # 发送请求
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,  # 使用json参数自动处理序列化
            timeout=60  # 图像生成可能需要更长时间
        )
        
        end_time = time.time()
        print(f"请求完成，耗时: {end_time - start_time:.2f} 秒")
        print(f"响应状态码: {response.status_code}")
        
        # 打印响应头
        print("\n响应头信息:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        # 检查响应状态
        if response.status_code == 200:
            # 成功响应
            try:
                data = response.json()
                print("\n响应JSON数据:")
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
                # 检查是否包含图像URL
                if 'data' in data and data['data']:
                    print("\n✅ 成功生成图像!")
                    for idx, item in enumerate(data['data']):
                        if 'url' in item:
                            print(f"  图像 {idx+1} URL: {item['url']}")
            except json.JSONDecodeError:
                print("\n⚠️  响应不是有效的JSON格式")
                print(f"原始响应内容: {response.text}")
        else:
            # 错误响应
            print("\n❌ 请求失败!")
            try:
                error_data = response.json()
                print("错误详情(JSON):")
                print(json.dumps(error_data, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                print("错误详情(文本):")
                print(response.text)
                
    except requests.Timeout:
        print("\n❌ 请求超时!")
        print("可能是网络延迟或服务器处理时间过长")
    except requests.ConnectionError:
        print("\n❌ 网络连接错误!")
        print("无法连接到API服务器，请检查网络设置和防火墙")
    except requests.RequestException as e:
        print(f"\n❌ 请求异常: {str(e)}")
        print("异常详情:")
        print(traceback.format_exc())
    except Exception as e:
        print(f"\n❌ 发生未知错误: {str(e)}")
        print("异常详情:")
        print(traceback.format_exc())
    finally:
        print("\n===== 调试结束 =====")

if __name__ == "__main__":
    debug_image_generation()