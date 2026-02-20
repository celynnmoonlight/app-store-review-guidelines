# -*- coding: utf-8 -*-
"""
修复 Apple App Store 审核指南文档中的格式问题
只修复 **** 和多余的 ** 符号
"""

import re

def fix_format(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 只修复 **** -> 空格
    content = content.replace('****', ' ')
    
    # 修复 **文字** 前后多余的空格
    # 例如：** 文字** -> **文字**
    content = re.sub(r'\*\*\s+([^\*])', r'**\1', content)
    content = re.sub(r'([^\*])\s+\*\*', r'\1**', content)
    
    # 清理多余空格（但保留换行）
    lines = content.split('\n')
    result = []
    for line in lines:
        # 只清理行内的多余空格，不改变行结构
        line = re.sub(r' +', ' ', line)
        result.append(line)
    
    content = '\n'.join(result)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"修复完成: {output_file}")
    print(f"行数: {len(result)}")

if __name__ == '__main__':
    input_file = 'd:\\MatlabProjects\\app-store-review-guidelines\\apple_app_store_review_guidelines.md'
    output_file = 'd:\\MatlabProjects\\app-store-review-guidelines\\apple_app_store_review_guidelines.md'
    fix_format(input_file, output_file)
