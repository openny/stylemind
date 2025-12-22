from pecab import PeCab
import kss
import re


class StyleAnalyzer:
    def __init__(self):
        self.pecab = PeCab()

    def analyze(self, text: str):
        if not text: return None

        # 1. 문장 분리
        sentences = kss.split_sentences(text)
        if not sentences: return None

        # 2. 통계적 특징 추출
        total_len = sum(len(s) for s in sentences)
        avg_len = total_len / len(sentences)

        # 3. 종결어미 분석 (Mecab 태그 EF: 종결어미)
        endings = []
        honorific_score = 0  # 높임말 점수

        for sent in sentences:
            pos = self.pecab.pos(sent)
            # 문장의 마지막 형태소 확인
            if pos:
                last_word, last_tag = pos[-1]
                if last_tag.startswith('EF') or last_tag == 'SF':  # SF는 마침표 등
                    # 그 앞의 실질적 어미를 찾기 위해 역순 탐색
                    for w, t in reversed(pos):
                        if t.startswith('EF'):
                            endings.append(w)
                            if '요' in w or '습니다' in w or 'ㅂ니다' in w:
                                honorific_score += 1
                            break

        # 말투 비율 계산
        is_polite = (honorific_score / len(sentences)) > 0.5 if sentences else False
        top_endings = sorted(endings, key=endings.count, reverse=True)[:3]

        return {
            "avg_length": round(avg_len, 1),
            "is_polite": is_polite,
            "top_endings": top_endings,
            "style_prompt": self._generate_prompt(avg_len, is_polite, top_endings)
        }

    def _generate_prompt(self, avg_len, is_polite, top_endings):
        tone = "친절하고 정중한 존댓말(해요체/십시오체)" if is_polite else "친근하거나 독백조의 반말(해체/해라체)"
        len_style = "짧고 간결하게" if avg_len < 30 else "상세하고 호흡이 긴 문장으로"
        return f"""
        [작성 가이드]
        1. 말투: {tone}을 반드시 유지하세요.
        2. 자주 사용하는 종결어미: '{", ".join(top_endings)}' 등을 적절히 섞어 쓰세요.
        3. 문장 길이: 평균 {avg_len}자 내외로 {len_style} 작성하세요.
        4. 문맥: 사용자의 경험을 공유하는 자연스러운 블로그 톤앤매너를 유지하세요.
        """