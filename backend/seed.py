"""Demo data seeder — populates data matching the WF01-WF04 wireframes
(Redeemed Group of Schools, Form 2B Young Investors track) so the frontend
has something real to render against.

Usage: python seed.py
"""
import random
from datetime import datetime, timedelta

from app import create_app
from app.extensions import db
from app.models import (
    User,
    Role,
    AccountType,
    AgeGroup,
    School,
    SchoolClass,
    Programme,
    Module,
    Lesson,
    Quiz,
    QuizQuestion,
    QuizChoice,
    LessonProgress,
    QuizAttempt,
    Certificate,
)

app = create_app()


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        super_admin = User(
            role=Role.SUPER_ADMIN,
            account_type=AccountType.PROFESSIONAL,
            age_group=AgeGroup.PROFESSIONAL,
            name="Alec Kamukombe",
            email="alec@nextgenacademy.co.zw",
        )
        super_admin.set_password("changeme")
        db.session.add(super_admin)

        school_admin = User(
            role=Role.SCHOOL_ADMIN,
            account_type=AccountType.SCHOOL,
            age_group=AgeGroup.PROFESSIONAL,
            name="Peace Pundu",
            email="peace@redeemedschools.co.zw",
        )
        school_admin.set_password("changeme")
        db.session.add(school_admin)
        db.session.flush()

        school = School(name="Redeemed Group of Schools", term_label="Term 2, 2026", academic_year=2026)
        db.session.add(school)
        db.session.flush()
        school_admin.school_id = school.id

        teacher = User(
            role=Role.TEACHER,
            account_type=AccountType.SCHOOL,
            age_group=AgeGroup.PROFESSIONAL,
            name="Mr Moyo",
            email="moyo@redeemedschools.co.zw",
            school_id=school.id,
        )
        teacher.set_password("changeme")
        db.session.add(teacher)
        db.session.flush()

        programme = Programme(title="Young Investors Track", age_group="13-18", description="ZSE & VFEX investing for teens")
        db.session.add(programme)
        db.session.flush()

        module_titles = [
            "Money & the Economy",
            "Budgeting & Saving",
            "ZSE & VFEX Investing",
            "Risk & Bad Debt",
            "Building Wealth",
        ]
        modules = []
        for i, title in enumerate(module_titles):
            m = Module(programme_id=programme.id, title=title, order=i)
            db.session.add(m)
            modules.append(m)
        db.session.flush()

        # Module 3 gets full lesson detail matching WF04
        m3_lessons = [
            ("What is investing?", 300, [
                {"term": "Investing", "definition": "Putting money to work to grow it over time."},
            ]),
            ("Types of investments in Zimbabwe", 360, []),
            ("Risk vs return — smart choices", 480, []),
            ("How the Zimbabwe Stock Exchange actually works", 444, [
                {"term": "Share / Stock", "definition": "A small piece of ownership in a company listed on the ZSE or VFEX"},
                {"term": "Market capitalisation", "definition": "Total value of all shares — share price x total shares in issue"},
                {"term": "Dividend", "definition": "A portion of company profit paid out to shareholders"},
                {"term": "VFEX", "definition": "Victoria Falls Stock Exchange — Zimbabwe's USD-denominated market"},
            ]),
            ("Reading a ZSE share price", 360, []),
            ("Building your first portfolio", 540, []),
        ]
        lessons = []
        for i, (title, duration, key_terms) in enumerate(m3_lessons):
            lesson = Lesson(
                module_id=modules[2].id,
                title=title,
                order=i,
                youtube_video_id="dQw4w9WgXcQ",
                duration_seconds=duration,
                workbook_url=f"/workbooks/young-investors-m3-l{i+1}.pdf",
                key_terms=key_terms,
                required_tier="school",
            )
            db.session.add(lesson)
            lessons.append(lesson)
        db.session.flush()

        for lesson in lessons:
            quiz = Quiz(lesson_id=lesson.id, passing_score_pct=60, coin_reward=150)
            db.session.add(quiz)
            db.session.flush()
            for qi in range(5):
                q = QuizQuestion(quiz_id=quiz.id, question_text=f"Sample question {qi+1} for {lesson.title}", order=qi)
                db.session.add(q)
                db.session.flush()
                for ci in range(4):
                    db.session.add(QuizChoice(question_id=q.id, text=f"Choice {ci+1}", is_correct=(ci == 0)))

        cls = SchoolClass(school_id=school.id, name="Form 2B — Young Investors", teacher_id=teacher.id, programme_id=programme.id)
        db.session.add(cls)
        db.session.flush()

        student_names = [
            "Tatenda Mhofu", "Rudo Chikwanda", "Farai Mutasa", "Nyasha Sibanda",
            "Tawanda Sibanda", "Zvikomborero Mpofu",
        ]
        students = []
        for i, full_name in enumerate(student_names):
            first, last = full_name.split(" ", 1)
            student = User(
                role=Role.STUDENT,
                account_type=AccountType.SCHOOL,
                age_group=AgeGroup.TEENS,
                name=full_name,
                username=f"{first}{last[0]}",
                school_id=school.id,
                class_id=cls.id,
                last_active_at=datetime.utcnow() - timedelta(days=[0, 1, 2, 5, 9, 0][i]),
            )
            student.set_pin(f"{random.randint(1000, 9999)}")
            db.session.add(student)
            students.append(student)
        db.session.flush()

        # Modules 1 & 2 fully completed, module 3 in progress per WF02
        for student in students:
            for m in modules[:2]:
                for lesson in m.lessons:
                    db.session.add(
                        LessonProgress(student_id=student.id, lesson_id=lesson.id, status="completed", completed_at=datetime.utcnow())
                    )
            for i, lesson in enumerate(lessons):
                status = "completed" if i < 3 else "in_progress" if i == 3 else "locked"
                db.session.add(LessonProgress(student_id=student.id, lesson_id=lesson.id, status=status))
                if status == "completed":
                    db.session.add(QuizAttempt(student_id=student.id, quiz_id=lesson.quiz.id, score_pct=random.randint(65, 95), passed=True))

            db.session.add(Certificate(student_id=student.id, module_id=modules[0].id))
            db.session.add(Certificate(student_id=student.id, module_id=modules[1].id))

        db.session.commit()
        print("Seed complete.")
        print(f"Super admin: {super_admin.email} / changeme")
        print(f"School admin: {school_admin.email} / changeme")
        print(f"Students (username / PIN not printed — reset via school admin flow)")


if __name__ == "__main__":
    run()
