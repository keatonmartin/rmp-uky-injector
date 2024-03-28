
// mutation observer for whole document
const globalObserver = new MutationObserver(mutations => {
    console.log("test");    
});

// initialize global observer
globalObserver.observe(document.body, { 
    subtree: true, 
    childList: true, 
    characterData: true, 
    attributes: true 
});