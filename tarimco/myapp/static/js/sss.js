document.addEventListener("DOMContentLoaded", function () {
  const firstAccordionItemHeader = document.querySelector(
    ".accordion-item-header"
  );
  const firstAccordionItemBody = firstAccordionItemHeader.nextElementSibling;

  // Open the first accordion item by default
  firstAccordionItemHeader.classList.add("active");
  firstAccordionItemBody.style.maxHeight =
    firstAccordionItemBody.scrollHeight + "px";

  const accordionItemHeaders = document.querySelectorAll(
    ".accordion-item-header"
  );

  accordionItemHeaders.forEach((accordionItemHeader) => {
    accordionItemHeader.addEventListener("click", (event) => {
      const currentlyActiveAccordionItemHeader = document.querySelector(
        ".accordion-item-header.active"
      );
      if (
        currentlyActiveAccordionItemHeader &&
        currentlyActiveAccordionItemHeader !== accordionItemHeader
      ) {
        currentlyActiveAccordionItemHeader.classList.toggle("active");
        currentlyActiveAccordionItemHeader.nextElementSibling.style.maxHeight = 0;
      }
      accordionItemHeader.classList.toggle("active");
      const accordionItemBody = accordionItemHeader.nextElementSibling;
      if (accordionItemHeader.classList.contains("active")) {
        accordionItemBody.style.maxHeight =
          accordionItemBody.scrollHeight + "px";
      } else {
        accordionItemBody.style.maxHeight = 0;
      }
    });
  });
});