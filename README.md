# ⚡ RacerAPI

**RacerAPI** is a lightweight, opinionated backend framework built on top of **FastAPI**.
It helps you start projects faster and keep them **organized, scalable, and maintainable** as they grow.

Think of RacerAPI as **FastAPI + structure + CLI**.

---

## ✨ What You Get

* 📁 **Clean project structure** (controllers, services, schemas)
* ⚙️ **CLI** to generate projects and modules
* 🧩 **Modular architecture** for large codebases
* 🧪 **Testing-ready setup**
* 🚀 **FastAPI performance**, no heavy abstractions
* 🔌 Easy to extend with auth, DB, AI, queues, etc.

---

## 📦 Install

```bash
pip install racerapi
```

---

## 🚀 Create a New Project

```bash
racerapi new myapp
cd myapp
racerapi dev
```

Your app runs at:

```
http://127.0.0.1:8000
```

---

## 📁 Project Structure

```text
app/
├── main.py
├── core/
│   ├── app_factory.py
│   ├── middleware.py
│   └── settings.py
├── modules/
│   └── users/
│       ├── controller.py
│       ├── service.py
│       ├── schemas.py
│       └── test/
```

Each **feature lives in its own module**.
This keeps your code easy to understand and easy to scale.

---

## 🧩 Example Controller

```python
from racerapi.core.decorators import Controller, Get

@Controller("system")
class SystemController:

    @Get("/health")
    async def health(self):
        return {"status": "ok"}
```

No FastAPI imports.
No router wiring.
Just business endpoints.

---

## ⚙️ CLI Commands

```bash
racerapi new <name>        # Create project
racerapi dev               # Start dev server
racerapi generate module   # Generate a module
racerapi doctor            # Validate project structure
racerapi routes            # List all routes
racerapi test              # Run tests
```

---

## 🧪 Testing

RacerAPI projects are **pytest-ready**.

```bash
racerapi test
```

Tests live next to the modules they test.

---

## 🧠 Why RacerAPI?

If you like FastAPI but want:

* Less boilerplate
* Fewer architecture decisions
* A consistent structure across projects

RacerAPI gives you that—**without hiding FastAPI** or locking you in.

---

## 🧱 Status

* Early-stage but stable core
* APIs may evolve
* Feedback and contributions welcome

---

## 📌 Summary

RacerAPI helps you:

* Start faster
* Stay organized
* Scale cleanly

**Build products, not project setups.**
