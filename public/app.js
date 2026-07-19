function formatDate(iso) {
  const [y, m, d] = iso.split("-");
  if (d === "00" || m === "00") return iso;
  const date = new Date(Number(y), Number(m) - 1, Number(d));
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  });
}

function decadeOf(year) {
  return Math.floor(year / 10) * 10;
}

function renderShow(show) {
  const article = document.createElement("article");
  article.className = "show";

  const headline = document.createElement("div");
  headline.className = "show-headline";

  const dateEl = document.createElement("time");
  dateEl.className = "show-date";
  dateEl.dateTime = show.date;
  dateEl.textContent = formatDate(show.date);

  const venueEl = document.createElement("span");
  venueEl.className = "show-venue";
  venueEl.textContent = show.venue;

  headline.appendChild(dateEl);
  headline.appendChild(document.createTextNode(" · "));
  headline.appendChild(venueEl);
  article.appendChild(headline);

  const placeEl = document.createElement("div");
  placeEl.className = "show-place";
  placeEl.textContent = show.place;
  article.appendChild(placeEl);

  if (show.notes) {
    const notes = document.createElement("div");
    notes.className = "show-notes";
    notes.textContent = show.notes;
    article.appendChild(notes);
  }

  if (show.recordings && show.recordings.length > 0) {
    const list = document.createElement("ul");
    list.className = "show-recordings";
    for (const rec of show.recordings) {
      const item = document.createElement("li");
      const link = document.createElement("a");
      link.href = rec.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = rec.title || rec.url;
      item.appendChild(link);
      item.appendChild(document.createTextNode(` (${rec.source})`));
      list.appendChild(item);
    }
    article.appendChild(list);
  }

  return article;
}

function renderDecadeNav(years) {
  const nav = document.getElementById("decades");
  nav.replaceChildren();

  const decades = [...new Set(years.map(decadeOf))].sort((a, b) => a - b);
  for (const decade of decades) {
    const link = document.createElement("a");
    link.href = `#decade-${decade}`;
    link.textContent = `${decade}s`;
    nav.appendChild(link);
  }
}

function renderShowsGrouped(shows) {
  const main = document.getElementById("shows");
  main.replaceChildren();

  let currentYear = null;
  let currentSection = null;
  let currentDecade = null;

  for (const show of shows) {
    const showDecade = decadeOf(show.year);

    if (showDecade !== currentDecade) {
      currentDecade = showDecade;
      const decadeMarker = document.createElement("div");
      decadeMarker.className = "decade-marker";
      decadeMarker.id = `decade-${showDecade}`;
      main.appendChild(decadeMarker);
    }

    if (show.year !== currentYear) {
      currentYear = show.year;
      currentSection = document.createElement("section");
      currentSection.className = "year-section";

      const heading = document.createElement("h2");
      heading.className = "year-heading";
      heading.id = `year-${show.year}`;
      heading.textContent = String(show.year);
      currentSection.appendChild(heading);

      const list = document.createElement("div");
      list.className = "year-shows";
      currentSection.appendChild(list);

      main.appendChild(currentSection);
    }

    currentSection.querySelector(".year-shows").appendChild(renderShow(show));
  }
}

async function loadShows() {
  const countEl = document.getElementById("count");
  const errorEl = document.getElementById("error");

  try {
    const res = await fetch("./data/shows.json");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();

    const recorded = data.shows.filter((s) => s.recordings && s.recordings.length > 0).length;
    countEl.textContent = `${data.count} shows · ${recorded} recorded`;
    renderDecadeNav(data.shows.map((s) => s.year));
    renderShowsGrouped(data.shows);
  } catch (err) {
    errorEl.hidden = false;
    errorEl.textContent = `Could not load shows: ${err.message}`;
  }
}

loadShows();
