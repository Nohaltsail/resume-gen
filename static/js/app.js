/* ===================== 动态增删条目 ===================== */
let photoBase64 = '';   // 最终传给后端的 base64（不含前缀）

function handlePhoto(input) {
  const file = input.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    photoBase64 = e.target.result.split(',')[1]; // 去掉 data:image/...;base64,
    const img = document.getElementById('photoImg');
    img.src = e.target.result;
    img.style.display = 'block';
    document.querySelector('#photoPreview .btn-remove').style.display = 'inline-block';
  };
  reader.readAsDataURL(file);
}

function removePhoto() {
  photoBase64 = '';
  document.getElementById('photoInput').value = '';
  document.getElementById('photoImg').style.display = 'none';
  document.querySelector('#photoPreview .btn-remove').style.display = 'none';
}

/* 教育背景 */
function addEducation() {
    const container = document.getElementById('educationEntries');
    const entry = document.createElement('div');
    entry.className = 'education-entry entry-item';
    entry.innerHTML = `
        <div class="form-row">
            <div class="form-field"><label>学历</label><input type="text" name="educationDegree[]" placeholder="例：计算机科学硕士" required></div>
            <div class="form-field"><label>时间</label><input type="text" name="educationPeriod[]" placeholder="例：2018-2022" required></div>
        </div>
        <div class="form-row">
            <div class="form-field"><label>学校</label><input type="text" name="educationSchool[]" placeholder="例：清华大学" required></div>
            <div class="form-field"><label>成绩</label><input type="text" name="educationGPA[]" placeholder="例：GPA 3.8/4.0"></div>
        </div>
        <button type="button" class="btn-remove" onclick="removeEducation(this)">删除</button>`;
    container.appendChild(entry);
}
function removeEducation(btn) {
    if (document.querySelectorAll('.education-entry').length > 1) btn.closest('.education-entry').remove();
    else alert('至少需要保留一个教育经历');
}

/* 工作经历 */
function addExperience() {
    const container = document.getElementById('experienceEntries');
    const entry = document.createElement('div');
    entry.className = 'experience-entry entry-item';
    entry.innerHTML = `
        <div class="form-row">
            <div class="form-field"><label>职位</label><input type="text" name="experienceTitle[]" placeholder="例：高级软件工程师" required></div>
            <div class="form-field"><label>时间</label><input type="text" name="experiencePeriod[]" placeholder="例：2020-至今" required></div>
        </div>
        <div class="form-row">
            <div class="form-field"><label>公司</label><input type="text" name="experienceCompany[]" placeholder="例：ABC科技有限公司" required></div>
            <div class="form-field"><label>地点</label><input type="text" name="experienceLocation[]" placeholder="例：北京"></div>
        </div>
        <div class="form-field"><label>工作描述</label><textarea name="experienceDescription[]" placeholder="描述你的工作职责和成就..." rows="3"></textarea></div>
        <button type="button" class="btn-remove" onclick="removeExperience(this)">删除</button>`;
    container.appendChild(entry);
}
function removeExperience(btn) {
    if (document.querySelectorAll('.experience-entry').length > 1) btn.closest('.experience-entry').remove();
    else alert('至少需要保留一个工作经历');
}

/* 技能专长 */
function addSkill() {
    const container = document.getElementById('skillEntries');
    const entry = document.createElement('div');
    entry.className = 'skill-entry entry-item';
    entry.innerHTML = `
        <div class="form-row">
            <div class="form-field"><label>技能名称</label><input type="text" name="skillName[]" placeholder="例：Java/Spring" required></div>
            <div class="form-field"><label>熟练程度 (1-20)</label><input type="number" name="skillLevel[]" min="1" max="20" value="10" required></div>
        </div>
        <button type="button" class="btn-remove" onclick="removeSkill(this)">删除</button>`;
    container.appendChild(entry);
}
function removeSkill(btn) {
    if (document.querySelectorAll('.skill-entry').length > 1) btn.closest('.skill-entry').remove();
    else alert('至少需要保留一个技能');
}

/* 项目经验 */
function addProject() {
    const container = document.getElementById('projectEntries');
    const entry = document.createElement('div');
    entry.className = 'project-entry entry-item';
    entry.innerHTML = `
        <div class="form-row">
            <div class="form-field"><label>项目名称</label><input type="text" name="projectName[]" placeholder="例：智能推荐系统" required></div>
            <div class="form-field"><label>时间</label><input type="text" name="projectPeriod[]" placeholder="例：2021.03-2021.12" required></div>
        </div>
        <div class="form-field"><label>项目描述</label><textarea name="projectDescription[]" placeholder="描述项目内容和你的贡献..." rows="3"></textarea></div>
        <button type="button" class="btn-remove" onclick="removeProject(this)">删除</button>`;
    container.appendChild(entry);
}
function removeProject(btn) {
    if (document.querySelectorAll('.project-entry').length > 1) btn.closest('.project-entry').remove();
    else alert('至少需要保留一个项目经历');
}

/* 个人荣誉 */
function addHonor() {
    const container = document.getElementById('honorEntries');
    const entry = document.createElement('div');
    entry.className = 'honor-entry entry-item';
    entry.innerHTML = `
        <div class="form-row">
            <div class="form-field"><label>奖项/荣誉名称</label><input type="text" name="honorName[]" placeholder="例：国家奖学金" required></div>
            <div class="form-field"><label>获得时间</label><input type="text" name="honorPeriod[]" placeholder="例：2022-10" required></div>
        </div>
        <button type="button" class="btn-remove" onclick="removeHonor(this)">删除</button>`;
    container.appendChild(entry);
}
function removeHonor(btn) {
    if (document.querySelectorAll('.honor-entry').length > 1) btn.closest('.honor-entry').remove();
    else alert('至少需要保留一条个人荣誉');
}

/* 外语水平 */
function addLanguage() {
    const container = document.getElementById('languageEntries');
    const entry = document.createElement('div');
    entry.className = 'language-entry entry-item';
    entry.innerHTML = `
        <div class="form-row">
            <div class="form-field"><label>语言</label><input type="text" name="languageName[]" placeholder="例：英语" required></div>
            <div class="form-field"><label>等级/分数</label><input type="text" name="languageLevel[]" placeholder="例：CET-6 560" required></div>
        </div>
        <button type="button" class="btn-remove" onclick="removeLanguage(this)">删除</button>`;
    container.appendChild(entry);
}
function removeLanguage(btn) {
    if (document.querySelectorAll('.language-entry').length > 1) btn.closest('.language-entry').remove();
    else alert('至少需要保留一条外语水平');
}

/* ===================== 业务逻辑 ===================== */
function toggleWorkExperience() {
    const isCampus = document.querySelector('input[name="recruitmentType"]:checked').value === 'campus';
    const workSec = document.getElementById('workExperienceSection');

    // 仅隐藏/显示 + 切换 required
    workSec.style.display = isCampus ? 'none' : 'block';
    workSec.querySelectorAll('input, textarea').forEach(el => {
        if (isCampus) el.removeAttribute('required');
        else el.setAttribute('required', '');
    });

    // 只在「校招且容器已空」时补一条空壳，社招不做任何预填充
    if (isCampus && workSec.querySelectorAll('.experience-entry').length === 0) {
        addExperience();
    }
}

/* 表单校验 */
function validateForm(d) {
    const err = [];
    if (!d.name) err.push('姓名');
    if (!d.jobTitle) err.push('求职职位');
    if (!d.phone) err.push('电话');
    if (!d.email) err.push('邮箱');

    const chkArr = (arr, label) => (arr || []).forEach((o, i) => {
        Object.keys(o).forEach(k => { if (!o[k]) err.push(`${label}第${i + 1}项的${k}`); });
    });

    chkArr(d.education, '教育背景');
    if (d.recruitmentType === 'social') chkArr(d.experience, '工作经历');
    chkArr(d.skills, '技能专长');
    chkArr(d.projects, '项目经验');
    chkArr(d.honors, '个人荣誉');
    chkArr(d.languages, '外语水平');
    return err;
}

/* 保存简历：本地 + 服务器 */
async function saveResume() {
    const data = collectFormData();
    localStorage.setItem('savedResume', JSON.stringify(data));
    const errors = validateForm(data);
    if (errors.length) {
        alert('简历已保存到本地存储！\n以下必填项尚未填写完整：\n' + errors.join('\n'));
        return;
    }
    try {
        const res = await fetch('/save-resume', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('服务器保存失败');
        alert('简历已保存到服务器和本地存储！');
    } catch (e) {
        alert('本地保存成功，服务器失败：' + e.message);
    }
}

/* 加载最近简历 */
async function loadLatestResume() {
    try {
        const type = document.querySelector('input[name="recruitmentType"]:checked').value;
        const res = await fetch(`/load-resume?recruitment_type=${type}`);
        if (!res.ok) throw new Error('网络错误');
        const data = await res.json();
        if (!data || (!data.name && !data.jobTitle)) {
            const keep = confirm('未找到最近简历，是否保留当前页面内容？\n（选“取消”将清空表单）');
            if (!keep) clearForm();
            return;
        }
        fillFormWithData(data);
    } catch (e) {
        console.error(e);
        const keep = confirm('加载失败，是否保留当前页面内容？\n（选“取消”将清空表单）');
        if (!keep) clearForm();
    }
}

/* 清空表单 */
function clearForm() {
    document.getElementById('resumeForm').reset();
    // 只清空条目，保留容器
    ['educationEntries', 'experienceEntries', 'skillEntries', 'projectEntries', 'honorEntries', 'languageEntries']
        .forEach(id => {
            const box = document.getElementById(id);
            if (box) box.innerHTML = '';
        });
    // 各留一条空壳
    addEducation();
    addExperience();
    addSkill();
    addProject();
    addHonor();
    addLanguage();
    toggleWorkExperience(); // 根据当前单选状态再切一次
}

/* 填充表单 */
function fillFormWithData(d) {
    /* 0. 先切换 DOM 可见性，再填数据，避免校招时操作被摘掉的 DOM */
    if (d.recruitmentType) {
        document.querySelector(`input[name="recruitmentType"][value="${d.recruitmentType}"]`).checked = true;
        toggleWorkExperience();          // 摘掉或恢复 DOM
    }

    /* 1. 基本信息 */
    ['name', 'jobTitle', 'phone', 'email', 'address', 'selfEvaluation']
        .forEach(id => { document.getElementById(id).value = d[id] || ''; });

    /* 2. 教育背景 */
    const eduBox = document.getElementById('educationEntries');
    eduBox.innerHTML = '';
    if (d.education?.length) d.education.forEach(o => {
        addEducation(); const e = eduBox.lastElementChild;
        e.querySelector('input[name="educationDegree[]"]').value = o.degree;
        e.querySelector('input[name="educationPeriod[]"]').value = o.period;
        e.querySelector('input[name="educationSchool[]"]').value = o.school;
        e.querySelector('input[name="educationGPA[]"]').value = o.gpa || '';
    }); else addEducation();

    /* 3. 工作经历（社招才填）*/
    if (document.getElementById('workExperienceSection').style.display !== 'none') {
        const expBox = document.getElementById('experienceEntries');
        expBox.innerHTML = '';                       // ① 先清空（关键）
        if (d.experience?.length) {
            // ② 逐条追加真实数据
            d.experience.forEach(o => {
                addExperience(); const e = expBox.lastElementChild;
                e.querySelector('input[name="experienceTitle[]"]').value = o.title;
                e.querySelector('input[name="experiencePeriod[]"]').value = o.period;
                e.querySelector('input[name="experienceCompany[]"]').value = o.company;
                e.querySelector('input[name="experienceLocation[]"]').value = o.location || '';
                e.querySelector('textarea[name="experienceDescription[]"]').value = o.description || '';
            });
        } else {
            // ③ 后端没返回 → 只留一条空壳
            addExperience();
        }
    }

    /* 4. 技能专长 */
    const skillBox = document.getElementById('skillEntries');
    skillBox.innerHTML = '';
    if (d.skills?.length) d.skills.forEach(o => {
        addSkill(); const e = skillBox.lastElementChild;
        e.querySelector('input[name="skillName[]"]').value = o.name;
        e.querySelector('input[name="skillLevel[]"]').value = o.level;
    }); else addSkill();

    /* 5. 项目经验 */
    const projBox = document.getElementById('projectEntries');
    projBox.innerHTML = '';
    if (d.projects?.length) d.projects.forEach(o => {
        addProject(); const e = projBox.lastElementChild;
        e.querySelector('input[name="projectName[]"]').value = o.name;
        e.querySelector('input[name="projectPeriod[]"]').value = o.period;
        e.querySelector('textarea[name="projectDescription[]"]').value = o.description || '';
    }); else addProject();

    /* 6. 个人荣誉 */
    const honorBox = document.getElementById('honorEntries');
    honorBox.innerHTML = '';
    if (d.honors?.length) d.honors.forEach(o => {
        addHonor(); const e = honorBox.lastElementChild;
        e.querySelector('input[name="honorName[]"]').value = o.name;
        e.querySelector('input[name="honorPeriod[]"]').value = o.period;
    }); else addHonor();

    /* 7. 外语水平 */
    const langBox = document.getElementById('languageEntries');
    langBox.innerHTML = '';
    if (d.languages?.length) d.languages.forEach(o => {
        addLanguage(); const e = langBox.lastElementChild;
        e.querySelector('input[name="languageName[]"]').value = o.name;
        e.querySelector('input[name="languageLevel[]"]').value = o.level;
    }); else addLanguage();

    /* 8. 模板选择 */
    if (d.template) {
        const radio = document.querySelector(`input[name="template"][value="${d.template}"]`);
        if (radio) radio.checked = true;
    }

    /* 9. 头像回显 */
    if (d.photo) {
        document.getElementById('photoImg').src = 'data:image/png;base64,' + d.photo;
        document.getElementById('photoImg').style.display = 'block';
        document.querySelector('#photoPreview .btn-remove').style.display = 'inline-block';
        photoBase64 = d.photo;
    } else {
        removePhoto();
    }
}

/* ===================== 预览 ===================== */
function previewResume() {
    document.getElementById('resumePreview').innerHTML = generateHTMLPreview(collectFormData());
}
function refreshPreview() { previewResume(); }

function generateHTMLPreview(d) {
    return `
    <div class="resume-html-preview">
        <div class="preview-header" style="background:#2c3e50;color:white;padding:30px;text-align:center;">
            <h1 style="margin:0;font-size:2.5em;">${d.name || '您的姓名'}</h1>
            <p style="margin:10px 0 0 0;font-size:1.2em;">${d.jobTitle || '求职职位'}</p>
        </div>
        <div style="padding:30px;display:grid;grid-template-columns:30% 70%;gap:30px;">
            <!-- 左侧 -->
            <div>
                <h3 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:5px;">联系方式</h3>
                <p><strong>电话:</strong> ${d.phone || ''}</p>
                <p><strong>邮箱:</strong> ${d.email || ''}</p>
                <p><strong>地址:</strong> ${d.address || ''}</p>

                <h3 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:5px;margin-top:20px;">技能专长</h3>
                ${d.skills?.map(s=>`
                    <div style="margin-bottom:10px;">
                        <div style="display:flex;justify-content:space-between;"><span>${s.name}</span><span>${s.level}/20</span></div>
                        <div style="background:#ecf0f1;height:8px;border-radius:4px;overflow:hidden;"><div style="background:#3498db;height:100%;width:${s.level*5}%"></div></div>
                    </div>`).join('')||'<p>暂无技能</p>'}

                <h3 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:5px;margin-top:20px;">外语水平</h3>
                ${d.languages?.map(l=>`<p><strong>${l.name}</strong>: ${l.level}</p>`).join('')||'<p>暂无外语信息</p>'}
            </div>
            <!-- 右侧 -->
            <div>
                <h3 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:5px;">教育背景</h3>
                ${d.education?.map(e=>`
                    <div style="margin-bottom:15px;">
                        <div style="display:flex;justify-content:space-between;"><strong>${e.degree}</strong><em>${e.period}</em></div>
                        <div style="display:flex;justify-content:space-between;"><span>${e.school}</span><span>${e.gpa||''}</span></div>
                    </div>`).join('')||'<p>暂无教育信息</p>'}

                ${d.recruitmentType!=='campus'&&d.experience?.length?`
                <h3 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:5px;margin-top:20px;">工作经历</h3>
                ${d.experience.map(exp=>`
                    <div style="margin-bottom:15px;">
                        <div style="display:flex;justify-content:space-between;"><strong>${exp.title}</strong><em>${exp.period}</em></div>
                        <div style="display:flex;justify-content:space-between;color:#666;"><span>${exp.company}</span><span>${exp.location||''}</span></div>
                        <p style="margin-top:5px;">${exp.description||''}</p>
                    </div>`).join('')}`:''}

                <h3 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:5px;margin-top:20px;">个人荣誉</h3>
                ${d.honors?.map(h=>`<p><strong>${h.name}</strong> – ${h.period}</p>`).join('')||'<p>暂无荣誉</p>'}

                <h3 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:5px;margin-top:20px;">项目经验</h3>
                ${d.projects?.map(p=>`
                    <div style="margin-bottom:15px;">
                        <div style="display:flex;justify-content:space-between;"><strong>${p.name}</strong><em>${p.period}</em></div>
                        <p style="margin-top:5px;">${p.description||''}</p>
                    </div>`).join('')||'<p>暂无项目</p>'}

                <h3 style="color:#2c3e50;border-bottom:2px solid #3498db;padding-bottom:5px;margin-top:20px;">自我评价</h3>
                <p style="white-space:pre-line">${d.selfEvaluation||'暂无自我评价'}</p>
            </div>
        </div>
    </div>`;
}

/* ===================== 数据收集 ===================== */
function collectFormData() {
    const f = new FormData(document.getElementById('resumeForm'));
    const type = document.querySelector('input[name="recruitmentType"]:checked').value;
    return {
        recruitmentType: type,
        name: f.get('name'),
        jobTitle: f.get('jobTitle'),
        phone: f.get('phone'),
        email: f.get('email'),
        address: f.get('address'),
        selfEvaluation: f.get('selfEvaluation'),
        education: [...document.querySelectorAll('.education-entry')].map(e => ({
            degree: e.querySelector('input[name="educationDegree[]"]').value,
            period: e.querySelector('input[name="educationPeriod[]"]').value,
            school: e.querySelector('input[name="educationSchool[]"]').value,
            gpa: e.querySelector('input[name="educationGPA[]"]').value
        })),
        experience: type === 'social' ? [...document.querySelectorAll('.experience-entry')].map(e => ({
            title: e.querySelector('input[name="experienceTitle[]"]').value,
            period: e.querySelector('input[name="experiencePeriod[]"]').value,
            company: e.querySelector('input[name="experienceCompany[]"]').value,
            location: e.querySelector('input[name="experienceLocation[]"]').value,
            description: e.querySelector('textarea[name="experienceDescription[]"]').value
        })) : [],
        skills: [...document.querySelectorAll('.skill-entry')].map(e => ({
            name: e.querySelector('input[name="skillName[]"]').value,
            level: +e.querySelector('input[name="skillLevel[]"]').value
        })),
        projects: [...document.querySelectorAll('.project-entry')].map(e => ({
            name: e.querySelector('input[name="projectName[]"]').value,
            period: e.querySelector('input[name="projectPeriod[]"]').value,
            description: e.querySelector('textarea[name="projectDescription[]"]').value
        })),
        honors: [...document.querySelectorAll('.honor-entry')].map(e => ({
            name: e.querySelector('input[name="honorName[]"]').value,
            period: e.querySelector('input[name="honorPeriod[]"]').value
        })),
        languages: [...document.querySelectorAll('.language-entry')].map(e => ({
            name: e.querySelector('input[name="languageName[]"]').value,
            level: e.querySelector('input[name="languageLevel[]"]').value
        })),
        photo: photoBase64,
        template: f.get('template')
    };
}

/* ===================== 提交 & 初始化 ===================== */
document.getElementById('resumeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = collectFormData();
    const errors = validateForm(data);
    if (errors.length) { alert('请完善以下项：\n' + errors.join('\n')); return; }

    const loading = document.getElementById('loading');
    loading.classList.remove('hidden');
    try {
        const res = await fetch('/generate-pdf', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('PDF生成失败');
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `${data.name || 'resume'}_简历.pdf`;
        document.body.appendChild(a); a.click();
        URL.revokeObjectURL(url);
    } catch (err) {
        alert('生成PDF出错：' + err.message);
    } finally {
        loading.classList.add('hidden');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    toggleWorkExperience();   // 默认校园招聘就摘掉
});

document.addEventListener('DOMContentLoaded', () => {
    toggleWorkExperience();
    // 如需要首次自动加载，可取消下行注释
    // loadLatestResume();
});