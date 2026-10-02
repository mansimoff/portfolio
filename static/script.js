"use strict";

/* ---- Мобильный сайдбар: раскрыть/свернуть контакты ---- */
const sidebar = document.querySelector("[data-sidebar]");
const sidebarBtn = document.querySelector("[data-sidebar-btn]");
if (sidebarBtn) {
  sidebarBtn.addEventListener("click", () => {
    const expanded = sidebar.getAttribute("data-sidebar-expanded") === "true";
    sidebar.setAttribute("data-sidebar-expanded", String(!expanded));
  });
}

/* ---- Табы (About / Resume / Portfolio / Certificates / Contact) ---- */
const navLinks = document.querySelectorAll("[data-nav-link]");
const pages = document.querySelectorAll("[data-page]");

navLinks.forEach((link) => {
  link.addEventListener("click", () => {
    const target = link.dataset.target;

    navLinks.forEach((l) => l.classList.remove("active"));
    link.classList.add("active");

    pages.forEach((page) => {
      page.classList.toggle("active", page.dataset.page === target);
    });

    window.scrollTo({ top: 0, behavior: "smooth" });
  });
});

/* ---- Фильтр проектов в Portfolio / Certificates ---- */
const filterBtns = document.querySelectorAll("[data-filter-btn]");
const projectItems = document.querySelectorAll("[data-filter-item]");

filterBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const filter = btn.dataset.filter;

    filterBtns.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");

    projectItems.forEach((item) => {
      const match = filter === "all" || item.dataset.category === filter;
      item.classList.toggle("active", match);
    });
  });
});

/* ---- Лайтбокс для сертификатов ---- */
/* Модалка в разметке не обязательна: если [data-lightbox] нет — создаём сами. */
let lightbox = document.querySelector("[data-lightbox]");

if (!lightbox) {
  lightbox = document.createElement("div");
  lightbox.className = "lightbox";
  lightbox.setAttribute("data-lightbox", "");
  lightbox.innerHTML = `
    <button class="lightbox-close" data-lightbox-close aria-label="Закрыть">&times;</button>
    <figure class="lightbox-content">
      <img data-lightbox-img src="" alt="">
      <figcaption>
        <strong data-lightbox-title></strong>
        <span data-lightbox-meta></span>
      </figcaption>
    </figure>`;
  document.body.appendChild(lightbox);
}

const lightboxImg = lightbox.querySelector("[data-lightbox-img]");
const lightboxTitle = lightbox.querySelector("[data-lightbox-title]");
const lightboxMeta = lightbox.querySelector("[data-lightbox-meta]");
const lightboxClose = lightbox.querySelector("[data-lightbox-close]");

function openLightbox({ img, title, meta }) {
  if (!img) return;
  lightboxImg.src = img;
  lightboxImg.alt = title || "certificate";
  lightboxTitle.textContent = title || "";
  lightboxMeta.textContent = meta || "";
  lightbox.classList.add("open");
  document.body.style.overflow = "hidden"; // блокируем скролл страницы
}

function closeLightbox() {
  if (!lightbox.classList.contains("open")) return;
  lightbox.classList.remove("open");
  document.body.style.overflow = "";
}

/* 1) Явные триггеры из разметки: элемент с data-cert-trigger + data-* атрибутами */
document.querySelectorAll("[data-cert-trigger]").forEach((item) => {
  item.addEventListener("click", (e) => {
    e.preventDefault();
    e.stopPropagation();
    openLightbox({
      img: item.dataset.img,
      title: item.dataset.title,
      meta: [item.dataset.issuer, item.dataset.year].filter(Boolean).join(" \u00b7 "),
    });
  });
});

/* 2) Автотриггеры: картинки внутри карточек сертификатов (текущий шаблон).
   Данные (название/эмитент/дата) подхватываются из соседних элементов карточки. */
document
  .querySelectorAll('.certificates [data-filter-item] figure, .certificates .cert-item figure, .certificates [data-cert-trigger]')
  .forEach((fig) => {
    if (fig.hasAttribute("data-cert-trigger")) return; // уже обработан выше
    const card = fig.closest("[data-filter-item], .cert-item");
    const img = fig.querySelector("img");
    if (!img) return;

    const title =
      card?.querySelector(".project-title, .cert-title")?.textContent.trim() || "";
    const meta = [...(card?.querySelectorAll(".project-category, .cert-meta") || [])]
      .map((el) => el.textContent.trim())
      .filter(Boolean)
      .join(" \u00b7 ");

    fig.addEventListener("click", (e) => {
      e.preventDefault();  // не переходим по ссылке, если карточка обёрнута в <a>
      e.stopPropagation();
      openLightbox({ img: img.src, title, meta });
    });
  });

/* Закрытие: крестик, клик по фону, Esc */
lightboxClose?.addEventListener("click", closeLightbox);
lightbox.addEventListener("click", (e) => {
  if (e.target === lightbox) closeLightbox(); // клик именно по фону, не по картинке
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeLightbox();
});
