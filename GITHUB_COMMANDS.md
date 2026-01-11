# 🔗 Команды для подключения к GitHub

## После создания репозитория на GitHub выполните:

### 1. Добавьте remote origin (замените YOUR_USERNAME на ваш GitHub username):

```bash
git remote add origin https://github.com/YOUR_USERNAME/bookstore-api-course.git
```

### 2. Переименуйте ветку в main:

```bash
git branch -M main
```

### 3. Отправьте код на GitHub:

```bash
git push -u origin main
```

## 🏷️ Создание тега для релиза:

```bash
# Create tag for first release
git tag -a v1.0.0 -m "Release v1.0.0 - Production-ready BookStore API Course

🎓 Complete Python development course from basics to production
🚀 FastAPI + Docker + Kubernetes + DevOps
📚 Full educational materials in Russian language
🧪 95%+ test coverage with comprehensive testing suite
🐳 Production-ready infrastructure with monitoring
⚡ From idea to production in 2 days"

# Push tag to GitHub
git push origin v1.0.0
```

## 📊 Проверка статуса:

```bash
# Check status
git status

# Check remote
git remote -v

# Check tags
git tag -l
```

## 🎯 После успешной публикации:

1. ✅ Репозиторий создан и код загружен
2. ✅ Создан релиз v1.0.0
3. ✅ Настроены topics и описание
4. ✅ Включены Issues, Wiki, Discussions

## 🌟 Поделитесь проектом:

- Добавьте ссылку в социальные сети
- Поделитесь с коллегами и друзьями
- Создайте пост в профессиональных сообществах
- Добавьте в портфолио

## 📈 Следующие шаги:

1. **Настройте GitHub Pages** для документации
2. **Создайте Issues** для будущих улучшений
3. **Включите Discussions** для сообщества
4. **Настройте branch protection** для main ветки
5. **Добавьте contributors** если работаете в команде