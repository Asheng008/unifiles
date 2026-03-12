import pytest
from unifiles import read_json, write_json, json_to_yaml, read_yaml

def test_read_write_json(tmp_path):
    """测试 JSON 读写"""
    data = {"name": "test", "value": 123, "list": [1, 2, 3], "cn": "中文"}
    file_path = tmp_path / "test.json"
    
    write_json(data, str(file_path))
    assert file_path.exists()
    
    # 检查文件内容是否包含中文（未转义）
    content = file_path.read_text(encoding="utf-8")
    assert "中文" in content
    
    read_data = read_json(str(file_path))
    assert read_data == data

def test_read_json_not_found():
    """测试读取不存在的 JSON 文件"""
    with pytest.raises(FileNotFoundError):
        read_json("nonexistent.json")

def test_json_to_yaml(tmp_path):
    """测试 JSON 转 YAML"""
    data = {"name": "test", "value": 123}
    json_path = tmp_path / "test.json"
    yaml_path = tmp_path / "test.yaml"
    
    write_json(data, str(json_path))
    json_to_yaml(str(json_path), str(yaml_path))
    
    assert yaml_path.exists()
    
    # 验证转换结果
    yaml_data = read_yaml(str(yaml_path))
    assert yaml_data == data
