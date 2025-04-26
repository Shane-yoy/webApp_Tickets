document.addEventListener("DOMContentLoaded", function () {
  // Sélectionner toutes les div à synchroniser
  const scrollableDivs = document.querySelectorAll(".chat-box, .chat-analyse");

  // Vérifiez si des divs sont trouvées
  if (scrollableDivs.length === 0) {
    console.error("Aucune div à synchroniser trouvée.");
    return;
  }

  console.log("Divs détectées :", scrollableDivs);

  // Fonction pour synchroniser le scroll
  function syncScroll(event) {
    const source = event.target;
    const scrollTop = source.scrollTop; // Position verticale
    const scrollHeight = source.scrollHeight; // Hauteur totale
    const clientHeight = source.clientHeight; // Hauteur visible

    console.log("Scroll détecté dans :", source.className);
    console.log(`ScrollTop: ${scrollTop}, ScrollHeight: ${scrollHeight}, ClientHeight: ${clientHeight}`);

    // Calculer le ratio de défilement
    const scrollRatio = scrollTop / (scrollHeight - clientHeight);

    // Appliquer ce ratio à toutes les autres divs
    scrollableDivs.forEach((div) => {
      if (div !== source) {
        div.scrollTop = scrollRatio * (div.scrollHeight - div.clientHeight);
      }
    });
  }

  // Attacher l'événement de défilement à chaque div
  scrollableDivs.forEach((div) => {
    div.addEventListener("scroll", syncScroll);
    console.log("Événement scroll attaché à :", div.className);
  });
});
