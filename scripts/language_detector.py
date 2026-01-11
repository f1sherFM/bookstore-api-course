#!/usr/bin/env python3
"""
Language detection utility for localization process.
Detects the language of text content to verify localization progress.
"""

import re
import string
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from collections import Counter


class LanguageDetector:
    """Detects language of text content using character patterns and common words."""
    
    def __init__(self):
        """Initialize language detector with pattern dictionaries."""
        # Common Russian words and patterns
        self.russian_words = {
            'и', 'в', 'не', 'на', 'я', 'быть', 'он', 'с', 'что', 'а', 'по', 'это', 'она', 'к', 'но',
            'они', 'мы', 'как', 'из', 'у', 'который', 'то', 'за', 'свой', 'что', 'её', 'так', 'вы',
            'сказать', 'этот', 'один', 'ещё', 'бы', 'такой', 'только', 'себя', 'своё', 'какой',
            'когда', 'уже', 'для', 'вот', 'кто', 'да', 'говорить', 'год', 'знать', 'мой', 'до',
            'или', 'если', 'время', 'рука', 'нет', 'самый', 'ни', 'стать', 'большой', 'даже',
            'другой', 'наш', 'свои', 'ну', 'под', 'где', 'дело', 'есть', 'сам', 'раз', 'чтобы',
            'два', 'там', 'чем', 'глаз', 'жизнь', 'первый', 'день', 'тут', 'во', 'ничто', 'потом',
            'очень', 'со', 'хотеть', 'ли', 'при', 'голова', 'надо', 'без', 'видеть', 'идти',
            'теперь', 'тоже', 'стоять', 'друг', 'дом', 'сейчас', 'можно', 'после', 'слово',
            'здесь', 'думать', 'место', 'спросить', 'через', 'работа', 'три', 'хорошо', 'новый',
            'жить', 'старый', 'хороший', 'каждый', 'правда', 'тогда', 'просто', 'нога', 'сидеть',
            'понять', 'иметь', 'конечно', 'делать', 'вдруг', 'над', 'взять', 'никто', 'сделать'
        }
        
        # Common English words
        self.english_words = {
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not',
            'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from',
            'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would',
            'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which',
            'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
            'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see',
            'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think',
            'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well',
            'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most',
            'us', 'is', 'water', 'long', 'very', 'after', 'call', 'man', 'here', 'old',
            'see', 'him', 'two', 'more', 'go', 'no', 'way', 'could', 'my', 'than', 'first',
            'been', 'call', 'who', 'oil', 'sit', 'now', 'find', 'down', 'day', 'did', 'get',
            'come', 'made', 'may', 'part'
        }
        
        # Cyrillic character range
        self.cyrillic_pattern = re.compile(r'[а-яё]', re.IGNORECASE)
        
        # Latin character range (excluding numbers and punctuation)
        self.latin_pattern = re.compile(r'[a-z]', re.IGNORECASE)
    
    def detect_text_language(self, text: str) -> Tuple[str, float]:
        """Detect language of text content.
        
        Args:
            text: Text to analyze
            
        Returns:
            Tuple of (language, confidence_score)
            language: 'russian', 'english', 'mixed', or 'unknown'
            confidence_score: 0.0 to 1.0
        """
        if not text.strip():
            return 'unknown', 0.0
        
        # Clean text for analysis
        clean_text = self._clean_text(text)
        
        if not clean_text:
            return 'unknown', 0.0
        
        # Count character types
        cyrillic_chars = len(self.cyrillic_pattern.findall(clean_text))
        latin_chars = len(self.latin_pattern.findall(clean_text))
        total_chars = cyrillic_chars + latin_chars
        
        if total_chars == 0:
            return 'unknown', 0.0
        
        # Calculate character ratios
        cyrillic_ratio = cyrillic_chars / total_chars
        latin_ratio = latin_chars / total_chars
        
        # Word-based detection
        words = self._extract_words(clean_text)
        russian_word_count = sum(1 for word in words if word.lower() in self.russian_words)
        english_word_count = sum(1 for word in words if word.lower() in self.english_words)
        
        # Combine character and word analysis
        russian_score = cyrillic_ratio * 0.7 + (russian_word_count / max(len(words), 1)) * 0.3
        english_score = latin_ratio * 0.7 + (english_word_count / max(len(words), 1)) * 0.3
        
        # Determine language
        if russian_score > 0.6:
            return 'russian', russian_score
        elif english_score > 0.6:
            return 'english', english_score
        elif russian_score > 0.3 and english_score > 0.3:
            return 'mixed', max(russian_score, english_score)
        else:
            return 'unknown', max(russian_score, english_score)
    
    def detect_file_language(self, file_path: str) -> Dict[str, any]:
        """Detect language of file content.
        
        Args:
            file_path: Path to file to analyze
            
        Returns:
            Dictionary with analysis results
        """
        path = Path(file_path)
        
        if not path.exists():
            return {
                'file': file_path,
                'error': 'File not found',
                'language': 'unknown',
                'confidence': 0.0
            }
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract text content based on file type
            text_content = self._extract_text_content(content, path.suffix)
            
            # Detect language
            language, confidence = self.detect_text_language(text_content)
            
            return {
                'file': file_path,
                'language': language,
                'confidence': confidence,
                'text_length': len(text_content),
                'total_length': len(content)
            }
            
        except Exception as e:
            return {
                'file': file_path,
                'error': str(e),
                'language': 'unknown',
                'confidence': 0.0
            }
    
    def analyze_directory(self, dir_path: str, extensions: Optional[List[str]] = None) -> List[Dict[str, any]]:
        """Analyze language of all files in directory.
        
        Args:
            dir_path: Directory path to analyze
            extensions: List of file extensions to analyze
            
        Returns:
            List of analysis results for each file
        """
        path = Path(dir_path)
        
        if not path.exists():
            return [{'error': f'Directory not found: {dir_path}'}]
        
        results = []
        for file_path in path.rglob("*"):
            if file_path.is_file():
                if extensions is None or file_path.suffix in extensions:
                    result = self.detect_file_language(str(file_path))
                    results.append(result)
        
        return results
    
    def _clean_text(self, text: str) -> str:
        """Clean text for language analysis."""
        # Remove code blocks, URLs, and technical content
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)  # Code blocks
        text = re.sub(r'`[^`]+`', '', text)  # Inline code
        text = re.sub(r'https?://\S+', '', text)  # URLs
        text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        
        return text.strip()
    
    def _extract_words(self, text: str) -> List[str]:
        """Extract words from text."""
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if len(word) > 2]  # Filter short words
    
    def _extract_text_content(self, content: str, file_extension: str) -> str:
        """Extract text content from file based on type."""
        if file_extension == '.py':
            # Extract comments and docstrings
            text_parts = []
            
            # Single line comments
            comments = re.findall(r'#\s*(.+)', content)
            text_parts.extend(comments)
            
            # Docstrings
            docstrings = re.findall(r'"""(.*?)"""', content, re.DOTALL)
            text_parts.extend(docstrings)
            
            # String literals (basic extraction)
            strings = re.findall(r'"([^"]+)"', content)
            strings.extend(re.findall(r"'([^']+)'", content))
            text_parts.extend(strings)
            
            return ' '.join(text_parts)
        
        elif file_extension in ['.md', '.txt']:
            # Markdown/text files - return full content
            return content
        
        elif file_extension in ['.yml', '.yaml']:
            # YAML comments
            comments = re.findall(r'#\s*(.+)', content)
            return ' '.join(comments)
        
        elif file_extension == '.sh':
            # Shell script comments
            comments = re.findall(r'#\s*(.+)', content)
            return ' '.join(comments)
        
        else:
            # Default: extract comments
            comments = re.findall(r'#\s*(.+)', content)
            return ' '.join(comments)


def main():
    """Command line interface for language detector."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Language detector for localization")
    parser.add_argument("--file", help="Analyze single file")
    parser.add_argument("--dir", help="Analyze directory")
    parser.add_argument("--extensions", nargs="+", help="File extensions to analyze")
    parser.add_argument("--text", help="Analyze text directly")
    parser.add_argument("--summary", action="store_true", help="Show summary statistics")
    
    args = parser.parse_args()
    
    detector = LanguageDetector()
    
    if args.text:
        language, confidence = detector.detect_text_language(args.text)
        print(f"Language: {language} (confidence: {confidence:.2f})")
    
    elif args.file:
        result = detector.detect_file_language(args.file)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"File: {result['file']}")
            print(f"Language: {result['language']} (confidence: {result['confidence']:.2f})")
            print(f"Text length: {result['text_length']} / {result['total_length']}")
    
    elif args.dir:
        results = detector.analyze_directory(args.dir, args.extensions)
        
        if args.summary:
            # Show summary statistics
            language_counts = Counter()
            total_files = 0
            
            for result in results:
                if 'error' not in result:
                    language_counts[result['language']] += 1
                    total_files += 1
            
            print(f"Total files analyzed: {total_files}")
            print("Language distribution:")
            for language, count in language_counts.most_common():
                percentage = (count / total_files) * 100 if total_files > 0 else 0
                print(f"  {language}: {count} files ({percentage:.1f}%)")
        else:
            # Show detailed results
            for result in results:
                if 'error' in result:
                    print(f"Error in {result.get('file', 'unknown')}: {result['error']}")
                else:
                    print(f"{result['file']}: {result['language']} ({result['confidence']:.2f})")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()