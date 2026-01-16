"""
Content Safety Module for Modern_USA_News
Filters profanity, validates content, and ensures quality standards
"""

import re
from typing import Dict, List, Tuple, Optional


class ContentSafety:
    """
    Content moderation and safety validation
    Features:
    - Profanity filtering
    - Bias detection
    - Rumor/speculation flagging
    - Quality validation
    """
    
    # Profanity patterns (censored for code cleanliness)
    PROFANITY_PATTERNS = [
        r'\bf[u*@]c?k\b', r'\bs[h*@]i?t\b', r'\ba[s*@]s\b', r'\bb[i*@]tch\b',
        r'\bd[a*@]mn\b', r'\bh[e*@]ll\b', r'\bcr[a*@]p\b', r'\bpi[s*@]s\b',
        r'\bwh[o*@]re\b', r'\bsl[u*@]t\b', r'\bd[i*@]ck\b', r'\bc[o*@]ck\b',
        r'\bb[a*@]st[a*@]rd\b'
    ]
    
    # Sensationalist language to avoid
    SENSATIONAL_WORDS = [
        'shocking', 'unbelievable', 'insane', 'crazy', 'explosive', 'bombshell',
        'devastating', 'destroy', 'destroyed', 'obliterate', 'annihilate',
        'catastrophic', 'horrific', 'terrifying', 'nightmare', 'slam', 'slammed',
        'blasted', 'ripped', 'eviscerated', 'demolished', 'crushed', 'epic',
        'you won\'t believe', 'wait until you see', 'must see'
    ]
    
    # Biased/opinion words
    BIASED_WORDS = [
        'evil', 'corrupt', 'criminal', 'liar', 'fraud', 'stupid', 'idiotic',
        'moron', 'fool', 'genius', 'hero', 'villain', 'savior', 'disaster',
        'best ever', 'worst ever', 'perfect', 'horrible', 'terrible',
        'obviously', 'clearly', 'everyone knows', 'the truth is'
    ]
    
    # Speculation markers
    SPECULATION_MARKERS = [
        'rumor has it', 'sources say', 'allegedly', 'reportedly', 'possibly',
        'might be', 'could be', 'may have', 'it is believed', 'unconfirmed',
        'anonymous source', 'insider says', 'leaked information'
    ]
    
    # Quality thresholds
    MIN_HEADLINE_WORDS = 3
    MAX_HEADLINE_WORDS = 12
    MIN_SUMMARY_WORDS = 5
    MAX_SUMMARY_WORDS = 22
    MIN_CAPTION_WORDS = 50
    MAX_CAPTION_LENGTH = 2200  # Instagram limit
    
    def __init__(self):
        self.issues = []
        self.modifications = []
        print("🛡️ Content Safety module initialized")
    
    def validate_and_clean(self, content: Dict[str, str]) -> Tuple[Dict[str, str], List[str]]:
        """
        Validate and clean content
        
        Args:
            content: Dict with 'headline', 'image_summary', 'caption', 'hashtags'
            
        Returns:
            Tuple of (cleaned_content, issues_found)
        """
        self.issues = []
        self.modifications = []
        
        cleaned = content.copy()
        
        # Clean each field
        if 'headline' in cleaned:
            cleaned['headline'] = self._clean_headline(cleaned['headline'])
        
        if 'image_summary' in cleaned:
            cleaned['image_summary'] = self._clean_summary(cleaned['image_summary'])
        
        if 'caption' in cleaned:
            cleaned['caption'] = self._clean_caption(cleaned['caption'])
        
        if 'hashtags' in cleaned:
            cleaned['hashtags'] = self._clean_hashtags(cleaned['hashtags'])
        
        return cleaned, self.issues
    
    def _clean_headline(self, text: str) -> str:
        """Clean and validate headline"""
        # Remove profanity
        text = self._filter_profanity(text)
        
        # Remove sensationalist language
        text = self._filter_sensational(text)
        
        # Check word count
        words = text.split()
        if len(words) < self.MIN_HEADLINE_WORDS:
            self.issues.append(f"Headline too short: {len(words)} words")
        elif len(words) > self.MAX_HEADLINE_WORDS:
            text = ' '.join(words[:self.MAX_HEADLINE_WORDS])
            self.modifications.append("Headline truncated to 12 words")
        
        # Remove emojis from headline
        text = self._remove_emojis(text)
        
        # Capitalize properly
        text = self._title_case(text)
        
        return text.strip()
    
    def _clean_summary(self, text: str) -> str:
        """Clean and validate image summary"""
        # Remove profanity
        text = self._filter_profanity(text)
        
        # Remove sensational language
        text = self._filter_sensational(text)
        
        # Check word count
        words = text.split()
        if len(words) > self.MAX_SUMMARY_WORDS:
            text = ' '.join(words[:self.MAX_SUMMARY_WORDS])
            self.modifications.append("Summary truncated to 22 words")
        
        # Remove emojis
        text = self._remove_emojis(text)
        
        return text.strip()
    
    def _clean_caption(self, text: str) -> str:
        """Clean and validate caption"""
        # Remove profanity
        text = self._filter_profanity(text)
        
        # Remove sensational language (but keep some in captions for engagement)
        text = self._soften_language(text)
        
        # Flag speculation
        self._check_speculation(text)
        
        # Check bias
        self._check_bias(text)
        
        # Validate length
        if len(text) > self.MAX_CAPTION_LENGTH:
            # Truncate at sentence boundary
            text = self._truncate_at_sentence(text, self.MAX_CAPTION_LENGTH)
            self.modifications.append("Caption truncated to fit Instagram limit")
        
        # Validate word count
        words = text.split()
        if len(words) < self.MIN_CAPTION_WORDS:
            self.issues.append(f"Caption may be too short: {len(words)} words")
        
        return text.strip()
    
    def _clean_hashtags(self, text: str) -> str:
        """Clean and validate hashtags"""
        # Split into individual hashtags
        hashtags = re.findall(r'#\w+', text)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_hashtags = []
        for tag in hashtags:
            tag_lower = tag.lower()
            if tag_lower not in seen:
                seen.add(tag_lower)
                unique_hashtags.append(tag)
        
        # Limit to 30 hashtags (Instagram limit)
        if len(unique_hashtags) > 30:
            unique_hashtags = unique_hashtags[:30]
            self.modifications.append("Hashtags limited to 30")
        
        return ' '.join(unique_hashtags)
    
    def _filter_profanity(self, text: str) -> str:
        """Remove profanity from text"""
        original = text
        
        for pattern in self.PROFANITY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                text = re.sub(pattern, '***', text, flags=re.IGNORECASE)
                self.modifications.append(f"Removed profanity: {matches[0]}")
        
        return text
    
    def _filter_sensational(self, text: str) -> str:
        """Remove sensationalist language"""
        text_lower = text.lower()
        
        for word in self.SENSATIONAL_WORDS:
            if word in text_lower:
                # Replace with neutral alternatives
                replacements = {
                    'shocking': 'notable',
                    'unbelievable': 'significant',
                    'insane': 'notable',
                    'crazy': 'unusual',
                    'explosive': 'significant',
                    'bombshell': 'major',
                    'devastating': 'significant',
                    'slam': 'criticize',
                    'slammed': 'criticized',
                    'blasted': 'criticized',
                    'ripped': 'criticized',
                    'demolished': 'challenged',
                    'crushed': 'defeated',
                    'epic': 'major'
                }
                
                replacement = replacements.get(word, '')
                if replacement:
                    text = re.sub(rf'\b{word}\b', replacement, text, flags=re.IGNORECASE)
                    self.modifications.append(f"Replaced '{word}' with '{replacement}'")
        
        return text
    
    def _soften_language(self, text: str) -> str:
        """Soften overly aggressive language in captions"""
        # Allow some engagement language but soften extremes
        softening = {
            'destroyed': 'criticized',
            'annihilated': 'defeated',
            'obliterated': 'overcame',
            'nightmare': 'difficult situation',
            'catastrophic': 'serious',
            'horrific': 'concerning',
            'terrifying': 'concerning'
        }
        
        for strong, soft in softening.items():
            if strong in text.lower():
                text = re.sub(rf'\b{strong}\b', soft, text, flags=re.IGNORECASE)
        
        return text
    
    def _check_speculation(self, text: str):
        """Flag speculation markers"""
        text_lower = text.lower()
        
        for marker in self.SPECULATION_MARKERS:
            if marker in text_lower:
                self.issues.append(f"Contains speculation marker: '{marker}'")
    
    def _check_bias(self, text: str):
        """Check for biased language"""
        text_lower = text.lower()
        
        found_bias = []
        for word in self.BIASED_WORDS:
            if word in text_lower:
                found_bias.append(word)
        
        if found_bias:
            self.issues.append(f"May contain biased language: {', '.join(found_bias[:3])}")
    
    def _remove_emojis(self, text: str) -> str:
        """Remove emojis from text (for headlines/summaries) """
        # Emoji regex pattern
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        return emoji_pattern.sub('', text)
    
    def _title_case(self, text: str) -> str:
        """Proper title case (not capitalizing small words) """
        small_words = {'a', 'an', 'the', 'and', 'but', 'or', 'for', 'nor', 
                       'on', 'at', 'to', 'by', 'in', 'of'}
        
        words = text.split()
        result = []
        
        for i, word in enumerate(words):
            if i == 0 or word.lower() not in small_words:
                result.append(word.capitalize())
            else:
                result.append(word.lower())
        
        return ' '.join(result)
    
    def _truncate_at_sentence(self, text: str, max_length: int) -> str:
        """Truncate text at sentence boundary"""
        if len(text) <= max_length:
            return text
        
        # Find sentence boundaries within limit
        truncated = text[:max_length]
        
        # Find last sentence end
        for punct in ['.', '!', '?']:
            last_punct = truncated.rfind(punct)
            if last_punct > max_length * 0.7:  # At least 70% of max
                return truncated[:last_punct + 1]
        
        # Fallback: truncate at word boundary
        last_space = truncated.rfind(' ')
        if last_space > 0:
            return truncated[:last_space] + '...'
        
        return truncated
    
    def get_quality_score(self, content: Dict[str, str]) -> int:
        """
        Calculate quality score (0-100)
        """
        score = 100
        
        # Deduct for issues
        score -= len(self.issues) * 5
        
        # Check headline quality
        headline = content.get('headline', '')
        if len(headline.split()) < 5:
            score -= 10
        
        # Check caption quality
        caption = content.get('caption', '')
        if len(caption.split()) < 100:
            score -= 15
        
        # Check for question at end (engagement)
        if not caption.strip().endswith('?'):
            score -= 5
        
        return max(0, min(100, score))
    
    def generate_report(self) -> str:
        """Generate content safety report"""
        report = []
        report.append("=" * 40)
        report.append("CONTENT SAFETY REPORT")
        report.append("=" * 40)
        
        if self.issues:
            report.append("\n⚠️ Issues Found:")
            for issue in self.issues:
                report.append(f"  - {issue}")
        else:
            report.append("\n✅ No issues found")
        
        if self.modifications:
            report.append("\n🔧 Modifications Made:")
            for mod in self.modifications:
                report.append(f"  - {mod}")
        
        report.append("=" * 40)
        return '\n'.join(report)


# Singleton instance
_safety_instance = None

def get_safety() -> ContentSafety:
    """Get content safety instance"""
    global _safety_instance
    if _safety_instance is None:
        _safety_instance = ContentSafety()
    return _safety_instance


if __name__ == "__main__":
    # Test content safety
    safety = ContentSafety()
    
    test_content = {
        "headline": "SHOCKING: Biden SLAMMED Over Insane New Policy! 🔥🔥🔥",
        "image_summary": "President faces explosive criticism over controversial decision that will destroy the economy",
        "caption": """Breaking news! In a shocking development, sources say that the President 
        has allegedly made a terrible decision that will devastate the American economy.
        
        This is obviously a disaster waiting to happen. Everyone knows this is the worst 
        policy ever proposed by any administration.
        
        Rumor has it that the Treasury Secretary was reportedly furious about this decision.
        
        What do you think about this controversy?
        
        📰 Follow @modern_usa_news for more updates!
        
        #Politics #USA #Breaking #News""",
        "hashtags": "#Politics #USA #Breaking #News #USPolitics"
    }
    
    print("🔍 Testing Content Safety Module\n")
    print("Original Content:")
    print(f"  Headline: {test_content['headline']}")
    print(f"  Summary: {test_content['image_summary'][:60]}...")
    
    cleaned, issues = safety.validate_and_clean(test_content)
    
    print("\n" + safety.generate_report())
    
    print("\nCleaned Content:")
    print(f"  Headline: {cleaned['headline']}")
    print(f"  Summary: {cleaned['image_summary'][:60]}...")
    
    print(f"\n📊 Quality Score: {safety.get_quality_score(cleaned)}/100")
