import json
from typing import List
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)
from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    Unicode,
    Text,
    Boolean,
    LargeBinary,
    JSON,
)


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    description: Mapped[str] = mapped_column(Unicode(255), nullable=False)

    # Relationships
    topics: Mapped[List["Topic"]] = relationship(
        "Topic",
        back_populates="category",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


# If the user uses oauth salt and password are null.
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    avatar: Mapped[str] = mapped_column(Text, nullable=True)
    username: Mapped[str] = mapped_column(Unicode(50), nullable=False)
    fullname: Mapped[str] = mapped_column(Unicode(100), nullable=True)
    email: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    password: Mapped["LargeBinary"] = mapped_column(LargeBinary, nullable=True)
    salt: Mapped["LargeBinary"] = mapped_column(LargeBinary, nullable=True)
    valid: Mapped[bool] = mapped_column(Boolean, nullable=False)
    failed_attempts: Mapped[int] = mapped_column(Integer, nullable=False)
    type: Mapped[str] = mapped_column(
        Unicode(1), nullable=False
    )  # User type (U - User / M - Moderator / A - Admin)
    lockout_time: Mapped["DateTime"] = mapped_column(DateTime, nullable=True)
    ban_expires: Mapped["DateTime"] = mapped_column(DateTime, nullable=True)
    banned: Mapped[bool] = mapped_column(Boolean, nullable=False)
    ban_reason: Mapped[bool] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(Text, nullable=True)
    about: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, fullname={self.fullname!r}, type={self.type!r})"


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    views: Mapped[int] = mapped_column(Integer, nullable=False)
    created: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
    pinned: Mapped[bool] = mapped_column(Boolean, nullable=False)
    closed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    tags: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=True
    )

    # Relationships
    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates="topic", cascade="all, delete", lazy="selectin"
    )
    user: Mapped["User"] = relationship("User", lazy="selectin")
    category: Mapped["Category"] = relationship("Category", lazy="joined")

    def replies(self, _):
        return len(self.posts)


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    content: Mapped["JSON"] = mapped_column(JSON, nullable=False)
    created: Mapped["DateTime"] = mapped_column(DateTime, nullable=False)
    edited: Mapped[bool] = mapped_column(Boolean, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    topic_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("topics.id"), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", lazy="selectin")
    topic: Mapped["Topic"] = relationship("Topic", lazy="selectin")
    likes: Mapped[List["Like"]] = relationship("Like", viewonly=True, lazy="selectin")
    edits: Mapped[List["PostEdits"]] = relationship("PostEdits", cascade="all, delete")

    @validates("content")
    def validate_post_content(self, key, content):
        if json.loads(content):
            return content


class PostEdits(Base):
    __tablename__ = "post_edits"

    edited_post: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), primary_key=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True, nullable=False
    )
    date: Mapped["DateTime"] = mapped_column(DateTime, primary_key=True, nullable=False)
    previous_text: Mapped["JSON"] = mapped_column(JSON, nullable=False)
    current_text: Mapped["JSON"] = mapped_column(JSON, nullable=False)

    post: Mapped["Post"] = relationship("Post", viewonly=True)
    user: Mapped["User"] = relationship("User", lazy="selectin")

    def __repr__(self):
        return


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", lazy="selectin")
    post: Mapped["Post"] = relationship("Post", lazy="selectin")


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", lazy="selectin")
    post: Mapped["Post"] = relationship("Post", lazy="selectin")


class UserActivation(Base):
    __tablename__ = "user_activation"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    token: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship("User", lazy="selectin")


class PasswordReset(Base):
    __tablename__ = "password_reset"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=False, nullable=False
    )
    expires: Mapped["DateTime"] = mapped_column(
        DateTime, primary_key=False, nullable=False
    )
    token: Mapped[str] = mapped_column(Text, primary_key=True, nullable=False)

    user: Mapped["User"] = relationship("User", lazy="selectin")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    link: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[str] = mapped_column(Text, nullable=False)
    read: Mapped[bool] = mapped_column(Boolean, nullable=False)
    originator_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )

    originator: Mapped["User"] = relationship(
        "User", foreign_keys=originator_id, lazy="joined"
    )
    user: Mapped["User"] = relationship("User", foreign_keys=user_id, lazy="joined")


class Chat(Base):
    __tablename__ = "chats"

    date: Mapped["DateTime"] = mapped_column(DateTime, primary_key=True, nullable=False)
    content: Mapped["JSON"] = mapped_column(JSON, nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True, nullable=False
    )
    recipient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True, nullable=False
    )

    author: Mapped["User"] = relationship(
        "User", foreign_keys=author_id, lazy="selectin"
    )
    recipient: Mapped["User"] = relationship(
        "User", foreign_keys=recipient_id, lazy="selectin"
    )


class FlaggedPost(Base):
    __tablename__ = "flagged_posts"

    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("posts.id"), primary_key=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True, nullable=False
    )
    reason_id: Mapped[int] = mapped_column(Integer, nullable=False)
    reason_text: Mapped[str] = mapped_column(Text, nullable=True)

    post: Mapped["Post"] = relationship("Post", foreign_keys=post_id, lazy="selectin")
    user: Mapped["User"] = relationship("User", foreign_keys=user_id, lazy="selectin")
