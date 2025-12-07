import os
import re
import subprocess
from resume.model.resume_model import ResumeData


def escape_latex(text):
    """
    转义 LaTeX 特殊字符
    """
    # LaTeX 特殊字符及其转义形式
    escape_dict = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}'
    }

    pattern = re.compile('|'.join(re.escape(key) for key in escape_dict.keys()))
    return pattern.sub(lambda match: escape_dict[match.group()], text)


class LatexGenerator:
    def __init__(self):
        self.output_dir = r"..\generated"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_latex_content(self, data: ResumeData) -> str:
        """把 ResumeData 填进 BASE_TEMPLATE，返回完整 latex 源码"""
        # from urllib.parse import quote
        photo_url = data.photo if data.photo else ''
        if data.template == 'classic':
            if data.recruitment_type == 'campus':
                with open(os.path.join(os.path.dirname(__file__), 'template_campus.tex'), 'r', encoding='utf-8') as f:
                    base_template = f.read()
            else:
                with open(os.path.join(os.path.dirname(__file__), 'template.tex'), 'r', encoding='utf-8') as f:
                    base_template = f.read()
        elif data.template == 'modern':
            if data.recruitment_type == 'campus':
                with open(os.path.join(os.path.dirname(__file__), 'modern_campus.tex'), 'r', encoding='utf-8') as f:
                    base_template = f.read()
            else:
                with open(os.path.join(os.path.dirname(__file__), 'modern.tex'), 'r', encoding='utf-8') as f:
                    base_template = f.read()
        else:
            if data.recruitment_type == 'campus':
                with open(os.path.join(os.path.dirname(__file__), 'creative_campus.tex'), 'r', encoding='utf-8') as f:
                    base_template = f.read()
            else:
                with open(os.path.join(os.path.dirname(__file__), 'creative.tex'), 'r', encoding='utf-8') as f:
                    base_template = f.read()
        return (base_template
                .replace('{name}', data.name)
                .replace('{jobTitle}', data.job_title)
                .replace('{phone}', data.phone)
                .replace('{email}', data.email)
                .replace('{address}', data.address or '')
                .replace('{photo}', photo_url.replace('\\', '/'))
                .replace('{education}', self._build_education(data))
                .replace('{experience}', self._build_experience(data))
                .replace('{skills}', self._build_skills(data))
                .replace('{projects}', self._build_projects(data))
                .replace('{honors}', self._build_honors(data))
                .replace('{languages}', self._build_languages(data))
                .replace('{selfEvaluation}', self._build_self_evaluation(data)))

    def compile_latex_to_pdf(self, resume_id: str, latex_content: str) -> str:
        """编译 latex → pdf，返回最终 pdf 绝对路径"""
        tex_file = os.path.join(self.output_dir, f'resume_{resume_id}.tex')
        pdf_file = os.path.join(self.output_dir, f'resume_{resume_id}.pdf')

        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)

        proc = subprocess.run([
            'xelatex', '-interaction=nonstopmode',
            '-output-directory', self.output_dir, tex_file
        ], capture_output=True, timeout=30)

        if proc.returncode == 0 and os.path.exists(pdf_file):
            return pdf_file
        raise RuntimeError(f'xelatex 编译失败：{proc.stderr.decode()}')

    @staticmethod
    def _build_education(data: ResumeData) -> str:
        lines = []
        for edu in data.education:
            lines.append(r'\textbf{' + edu.degree + r'} \hfill \textit{' + edu.period + r'} \\')
            lines.append(r'\textbf{' + edu.school + '}' +
                         (r' \hfill ' + edu.gpa if edu.gpa else '') + r' \\')
            lines.append(r'\vspace{2mm}')
        return '\n'.join(lines)

    @staticmethod
    def _build_experience(data: ResumeData) -> str:
        lines = []
        for exp in data.experience:
            lines.append(r'\textbf{' + exp.title + r'} \hfill \textit{' + exp.period + r'} \\')
            lines.append(r'\textbf{' + exp.company + '}' +
                         (r' \hfill ' + exp.location if exp.location else '') + r' \\')
            if exp.description:
                lines.append(exp.description + r' \\')
            lines.append(r'\vspace{2mm}')
        return '\n'.join(lines)

    @staticmethod
    def _build_skills(data: ResumeData) -> str:
        """
        保持 demo.tex 里的 \skillbar 命令
        技能 level 1-20 → 0-20 传给 \skillbar
        """
        lines = []
        for sk in data.skills:
            lines.append(r'\textbf{' + sk.name + r'} \\')
            lines.append(r'\skillbar{' + str(sk.level) + r'} \\')
            lines.append(r'\vspace{2mm}')
        return '\n'.join(lines)

    @staticmethod
    def _build_projects(data: ResumeData) -> str:
        lines = []
        for p in data.projects:
            lines.append(r'\textbf{' + p.name + r'} \hfill \textit{' + p.period + r'} \\')
            if p.description:
                lines.append(escape_latex(p.description) + r' \\')
            lines.append(r'\vspace{2mm}')
        return '\n'.join(lines)

    @staticmethod
    def _build_honors(data: ResumeData) -> str:
        """个人荣誉 section，保持 itemize 紧凑格式"""
        if not data.honors:
            return r'\begin{itemize}[leftmargin=*,nosep,itemsep=2pt]\item 暂无荣誉\end{itemize}'
        items = [rf'\item {h.name} \hfill \textit{{{h.period}}}' for h in data.honors]
        return (r'\begin{itemize}[leftmargin=*,nosep,itemsep=2pt]' +
                '\n' + '\n'.join(items) + '\n' + r'\end{itemize}')

    @staticmethod
    def _build_languages(data: ResumeData) -> str:
        """外语水平 section，保持原有表格风格"""
        if not data.languages:
            return '暂无外语信息'
        items = [rf'\item \textbf{{{l.name}}} \hfill {l.level}' for l in data.languages]
        return (r'\begin{itemize}[leftmargin=*,nosep,itemsep=2pt]' +
                '\n' + '\n'.join(items) + '\n' + r'\end{itemize}')

    @staticmethod
    def _build_self_evaluation(data: ResumeData) -> str:
        return data.self_evaluation or '暂无自我评价'

