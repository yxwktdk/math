import json  

# 假设你的数据存储在一个变量中  
data = {  
    "unary": {  
        "strict": {  
            "Points-unary": {  
                "Existence": 39,  
                "Quantity": 2,  
                "Size Property": 0  
            },  
            "Line Segment-unary": {  
                "Existence": 40,  
                "Quantity": 11,  
                "Size Property": 21  
            },  
            "Angle-unary": {  
                "Existence": 23,  
                "Quantity": 8,  
                "Size Property": 34  
            },  
            "Triangle-unary": {  
                "Existence": 16,  
                "Quantity": 12,  
                "Size Property": 5  
            },  
            "Circle-unary": {  
                "Existence": 16,  
                "Quantity": 10,  
                "Size Property": 3  
            },  
            "Polygon-unary": {  
                "Existence": 4,  
                "Quantity": 1,  
                "Size Property": 0  
            },  
            "Arc-unary": {  
                "Existence": 12,  
                "Quantity": 0,  
                "Size Property": 4  
            },  
            "Sector-unary": {  
                "Existence": 8,  
                "Quantity": 1,  
                "Size Property": 0  
            }  
        },  
        "loose": {  
            "Points-unary": {  
                "Existence": 39,  
                "Quantity": 2,  
                "Size Property": 0  
            },  
            "Line Segment-unary": {  
                "Existence": 40,  
                "Quantity": 11,  
                "Size Property": 21  
            },  
            "Angle-unary": {  
                "Existence": 23,  
                "Quantity": 8,  
                "Size Property": 34  
            },  
            "Triangle-unary": {  
                "Existence": 16,  
                "Quantity": 12,  
                "Size Property": 5  
            },  
            "Circle-unary": {  
                "Existence": 16,  
                "Quantity": 10,  
                "Size Property": 3  
            },  
            "Polygon-unary": {  
                "Existence": 4,  
                "Quantity": 1,  
                "Size Property": 0  
            },  
            "Arc-unary": {  
                "Existence": 12,  
                "Quantity": 0,  
                "Size Property": 4  
            },  
            "Sector-unary": {  
                "Existence": 8,  
                "Quantity": 1,  
                "Size Property": 0  
            }  
        },  
        "counts": {  
            "Points-unary": {  
                "Existence": 39,  
                "Quantity": 15,  
                "Size Property": 0  
            },  
            "Line Segment-unary": {  
                "Existence": 62,  
                "Quantity": 28,  
                "Size Property": 22  
            },  
            "Angle-unary": {  
                "Existence": 41,  
                "Quantity": 19,  
                "Size Property": 58  
            },  
            "Triangle-unary": {  
                "Existence": 34,  
                "Quantity": 43,  
                "Size Property": 14  
            },  
            "Circle-unary": {  
                "Existence": 30,  
                "Quantity": 28,  
                "Size Property": 3  
            },  
            "Polygon-unary": {  
                "Existence": 14,  
                "Quantity": 7,  
                "Size Property": 0  
            },  
            "Arc-unary": {  
                "Existence": 13,  
                "Quantity": 8,  
                "Size Property": 4  
            },  
            "Sector-unary": {  
                "Existence": 8,  
                "Quantity": 5,  
                "Size Property": 0  
            }  
        }  
    },  
    "binary": {  
        "strict": {  
            "Points": {  
                "Points": 19,  
                "LineSegment": 26,  
                "Angle": 18,  
                "Triangle": 11,  
                "Circle": 1,  
                "Polygon": 1  
            },  
            "LineSegment": {  
                "LineSegment": 27,  
                "Angle": 12,  
                "Triangle": 19,  
                "Circle": 20,  
                "Polygon": 2  
            },  
            "Angle": {  
                "Angle": 30,  
                "Triangle": 11,  
                "Circle": 7,  
                "Polygon": 1  
            },  
            "Triangle": {  
                "Triangle": 0,  
                "Circle": 1,  
                "Polygon": 0  
            },  
            "Circle": {  
                "Circle": 0,  
                "Polygon": 1  
            },  
            "Polygon": {  
                "Polygon": 0  
            }  
        },  
        "loose": {  
            "Points": {  
                "Points": 19,  
                "LineSegment": 26,  
                "Angle": 18,  
                "Triangle": 11,  
                "Circle": 1,  
                "Polygon": 1  
            },  
            "LineSegment": {  
                "LineSegment": 27,  
                "Angle": 12,  
                "Triangle": 19,  
                "Circle": 20,  
                "Polygon": 2  
            },  
            "Angle": {  
                "Angle": 31,  
                "Triangle": 11,  
                "Circle": 7,  
                "Polygon": 1  
            },  
            "Triangle": {  
                "Triangle": 0,  
                "Circle": 1,  
                "Polygon": 0  
            },  
            "Circle": {  
                "Circle": 0,  
                "Polygon": 1  
            },  
            "Polygon": {  
                "Polygon": 0  
            }  
        },  
        "counts": {  
            "Points": {  
                "Points": 50,  
                "LineSegment": 52,  
                "Angle": 27,  
                "Triangle": 16,  
                "Circle": 4,  
                "Polygon": 4  
            },  
            "LineSegment": {  
                "LineSegment": 50,  
                "Angle": 21,  
                "Triangle": 25,  
                "Circle": 24,  
                "Polygon": 2  
            },  
            "Angle": {  
                "Angle": 67,  
                "Triangle": 26,  
                "Circle": 11,  
                "Polygon": 1  
            },  
            "Triangle": {  
                "Triangle": 0,  
                "Circle": 2,  
                "Polygon": 0  
            },  
            "Circle": {  
                "Circle": 0,  
                "Polygon": 2  
            },  
            "Polygon": {  
                "Polygon": 0  
            }  
        }  
    }  
}  

def count_distribution(data):  
    distribution = {  
        "unary": {},  
        "binary": {}  
    }  

    # 统计 unary 类别的 count 分布  
    for category, types in data["unary"].items():  
        if category in ["strict", "loose", "counts"]:  
            for type_name, counts in types.items():  
                distribution["unary"][type_name] = counts  

    # 统计 binary 类别的 count 分布  
    for category, types in data["binary"].items():  
        if category in ["strict", "loose", "counts"]:  
            for type_name, counts in types.items():  
                distribution["binary"][type_name] = counts  

    return distribution  

# 运行统计函数  
result_distribution = count_distribution(data)  

# 打印结果  
print(json.dumps(result_distribution, indent=2, ensure_ascii=False))