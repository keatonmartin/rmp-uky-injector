const COURSE_CLASS = ".clearfix.course-row.expanded-section.table-thin-row-event"

let csvData; // global to store csv data to be accessed in mutation observer
profIndex = new Map(); // index into csvData that is built once the csv is parsed.

// mutation observer for whole document
const globalObserver = new MutationObserver(mutations => {
    const profCards = document.querySelectorAll(COURSE_CLASS)

    for (i = 0; i < profCards.length; i++) {
        prof = profCards[i]

        // occasionally a <p> element begins the course row cards, we index from the end to avoid
        // grabbing the wrong element

        // if there are five children, it's likely the bottom an entry with two lines, like a lab or practicum
        // in this case, the name is the last element as there is no "Plan" or "Register" button

        console.log(prof.children.length)

        if (prof.children.length == 5) {
            profNameElem = prof.children.item(4).children.item(0)
        } else {
            profNameElem = prof.children.item(prof.children.length-3).children.item(0)
        }

        // try using only first and last name if not present in map
        profName = profNameElem.textContent
        if (!profIndex.has(profName)) {
            names = profName.split(" ")
            if (names.length > 2) {
                profName = names[0] + " " + names[2]
            }
        }
        

        if (profIndex.has(profName)) {

            //Adding hyperlink
	        const anchorElement = document.createElement('a');
	        anchorElement.textContent = profName;
	        anchorElement.href = csvData[profIndex.get(profName)].link;
	        anchorElement.target = "_blank";
	        profNameElem.innerHTML = '';
	        profNameElem.appendChild(anchorElement);

	        if (csvData[profIndex.get(profName)].quality != 0)
            profNameElem.insertAdjacentHTML('beforeend',
            "<br>Rating: <b>" + csvData[profIndex.get(profName)].quality + "</b>"
            )

            if (csvData[profIndex.get(profName)].quality == 0)
            profNameElem.insertAdjacentHTML('beforeend',
            "<br>Rating: N/A<b>" + "</b>"
            )

        }
    }

});

const url = chrome.runtime.getURL("../data/profs.csv");

Papa.parse(url, {
    download: true,
    header: true,
    complete: function(res) {
        // build prof index
        for (i = 0; i < res.data.length; i++) {
            profIndex.set(res.data[i].name, i)
        }
        csvData = res.data 
        // initialize global observer
        globalObserver.observe(document.body, { 
            subtree: true, 
            childList: true, 
            characterData: true, 
            attributes: true 
        });
    }
})

