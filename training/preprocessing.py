# training/preprocessing.py
import re
from pathlib import Path
from typing import List, Tuple

def preprocess_docker_docs(doc_path: str) -> List[str]:
    """Process Docker documentation files"""
    examples = []
    with open(doc_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Split into logical chunks
        sections = content.split('\n## ')
        for section in sections:
            if section.strip():
                # Create training examples from headers and content
                header = section.split('\n')[0].strip()
                content = '\n'.join(section.split('\n')[1:])
                
                # Add context information
                example = f"Docker Documentation\nSection: {header}\nContent:\n{content}"
                examples.append(example)
    
    return examples

def preprocess_go_code(code_path: str) -> List[Tuple[str, str]]:
    """Process Go source code files"""
    examples = []
    with open(code_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        current_function = ""
        current_doc = ""
        
        for line in lines:
            if line.strip().startswith('//'):
                # Documentation comment
                current_doc += line.strip()[2:] + "\n"
            elif line.strip().startswith('func'):
                # Function definition
                if current_function:
                    examples.append((current_function, current_doc.strip()))
                current_function = line.strip()
                current_doc = ""
            else:
                current_function += line
                
        # Add last function
        if current_function:
            examples.append((current_function, current_doc.strip()))
    
    return examples