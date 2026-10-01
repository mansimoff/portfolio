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

/* ---- Фильтр проектов в Portfolio ---- */
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
const lightbox = document.querySelector("[data-lightbox]");
const lightboxImg = document.querySelector("[data-lightbox-img]");
const lightboxTitle = document.querySelector("[data-lightbox-title]");
const lightboxMeta = document.querySelector("[data-lightbox-meta]");
const lightboxClose = document.querySelector("[data-lightbox-close]");

document.querySelectorAll("[data-cert-trigger]").forEach((item) => {
  item.addEventListener("click", () => {
    lightboxImg.src = item.dataset.img;
    lightboxImg.alt = item.dataset.title;
    lightboxTitle.textContent = item.dataset.title;
    const issuer = item.dataset.issuer || "";
    const year = item.dataset.year || "";
    lightboxMeta.textContent = [issuer, year].filter(Boolean).join(" · ");
    lightbox.classList.add("open");
  });
});

function closeLightbox() {
  lightbox.classList.remove("open");
}
lightboxClose?.addEventListener("click", closeLightbox);
lightbox?.addEventListener("click", (e) => {
  if (e.target === lightbox) closeLightbox();
});
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeLightbox();
});
