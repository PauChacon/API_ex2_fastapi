document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    fetch("http://localhost:8000/alumne/list")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; // Netejar la taula abans d'afegir res

            // Iterar sobre los alumnos y agregarlos al DOM
            data.forEach(alumne => {
                const row = document.createElement("tr");

                // Nom
                const nomAluCell = document.createElement("td");
                nomAluCell.textContent = alumne.nomAlumne;  // 'nomAlumne' es el nombre del alumno en el JSON
                row.appendChild(nomAluCell);

                // Cicle
                const cicleAluCell = document.createElement("td");
                cicleAluCell.textContent = alumne.cicle;  // 'cicle' es el campo del ciclo
                row.appendChild(cicleAluCell);

                // Curs
                const cursAluCell = document.createElement("td");
                cursAluCell.textContent = alumne.curs;  // 'curs' es el curso
                row.appendChild(cursAluCell);

                // Grup
                const grupAluCell = document.createElement("td");
                grupAluCell.textContent = alumne.grup;  // 'grup' es el grupo
                row.appendChild(grupAluCell);

                // Nom de l'aula (DescAula)
                const descAulaCell = document.createElement("td");
                descAulaCell.textContent = alumne.DescAula;  // 'DescAula' es la descripción del aula
                row.appendChild(descAulaCell);

                // Afegir la fila a la taula
                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});
