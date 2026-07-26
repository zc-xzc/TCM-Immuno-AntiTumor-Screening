import http.client

# 测试Web服务器是否正常运行
def test_server():
    conn = http.client.HTTPConnection("localhost", 5000, timeout=5)
    try:
        conn.request("GET", "/models")
        response = conn.getresponse()
        print(f"状态码: {response.status}")
        print(f"响应头: {response.getheaders()}")
        content = response.read()
        print(f"响应内容: {content.decode()}")
        conn.close()
        return True
    except Exception as e:
        print(f"测试失败: {e}")
        conn.close()
        return False

if __name__ == "__main__":
    test_server()