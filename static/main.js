const getClick = (goForward = true) => () => {
  const urlParams = new URLSearchParams(window.location.search);
  const rows = +urlParams.get("rows") || 25;
  const page = +urlParams.get("page") || 1;

  const actualPage = window.location.href;
  const newPageBase = actualPage.split("profiles")[0];

  const modifier = goForward ? 1 : page > 1 ? -1 : 0;

  window.location.href = `${newPageBase}profiles?rows=${rows}&page=${
    modifier + page
  }`;
};

const prevBtns = document.getElementsByName("btn-prev");
prevBtns.forEach((btn) => btn.addEventListener("click", getClick(false)));

const nextBtns = document.getElementsByName("btn-next");
nextBtns.forEach((btn) => btn.addEventListener("click", getClick(true)));
