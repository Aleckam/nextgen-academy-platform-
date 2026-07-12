from datetime import datetime

from app.extensions import db


class BlogPost(db.Model):
    __tablename__ = "blog_posts"

    CATEGORIES = [
        "Kids & Money",
        "ZSE & Investing",
        "Zimbabwe Focus",
        "AI & Finance",
        "Financial Literacy",
    ]

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    excerpt = db.Column(db.String(400))
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="draft")  # draft | published
    published_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "category": self.category,
            "excerpt": self.excerpt,
            "status": self.status,
            "published_at": self.published_at.isoformat() if self.published_at else None,
        }


class NewsletterSignup(db.Model):
    __tablename__ = "newsletter_signups"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
