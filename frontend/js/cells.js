// Programmatic position labeling based on id for div="aix-grid-box-child"
const labelCellPositions = async () => {
  // This makes the frontend HTML very pleasant to work with
  // First, target parent ID, e.g. 'aix-grid-box-9-9' for 9x9 box
  // Then, target its direct children
  // Then, get ID for all of the direct child elements
  const returnBoxAll = async () => {
    if (BoxType === 9) {
      return document.getElementById("aix-grid-box-9-9")
    } else if (BoxType === 8) {
      return document.getElementById("aix-grid-box-8-8")
    } else if (BoxType === 10) {
      return document.getElementById("aix-grid-box-10-10")
    }
  }

  const boxAll = await returnBoxAll()
  const boxChildren = Array.from(boxAll.children)
  const boxChildrenId = boxChildren.map(element => { return element.id })

  // element.id is in the form of "cell_{id}", we just need {id}
  const boxChildrenIdLabel = boxChildrenId.map(cell => { return cell.split("_")[1] })

  // Using for ... of syntax with index counting
  for (const [index, value] of boxChildrenId.entries()) {
    span_target = document.getElementById(value)
    span_target.innerHTML = `
      <span class="aix-grid-cell-pos">
        ${boxChildrenIdLabel[index]}
      </span>
    `
  }
}


// Function to clear view if no URLSearchParams detected
const ClearView = () => {
  // TODO: for fetchVialData when no search param detected
  console.log("Haha! No search param!")
}


//  Fetch data from REST API server
const fetchVialData = async () => {
  // get url parameters
  const params = new URLSearchParams(window.location.search)
  const box_id = params.get('box_id')

  // TODO:
  // if no search param detected, return something to communicate the error!

  // Get those data!
  try {
    const response = await fetch(`${ApiUrl}/vials/${box_id}`)
    const data = await response.json()
    // console.log(data)
    return data
  } catch (error) {
    console.error(error)
  }
}


// For position with data, add information
const markCells = async () => {
  // Default text content when no cell is hovered on
  const hoverTextContent = ""
  let vialInfo = document.getElementById("aix-content-listing-cell")
  vialInfo.innerHTML = hoverTextContent

  // First, we obtain vial data from fetchVialData()
  let currentVialData = fetchVialData()

  // Elegantly loop over each element within the currentVialData
  currentVialData.then(vials => {
    const vialData = vials.cellArray

    // Only take the index (idx)
    for (const [idx, _] of vialData.entries()) {
      let vialPosition = `cell_${vialData[idx]['Position']}`

      // Update text content within each cell position
      let vialCell = document.getElementById(vialPosition)
      vialCell.innerHTML += `
        <span class="aix-grid-cell-label">
          ${vialData[idx]['shortName']}
        <span>

        <span class="aix-grid-cell-label-date">
          ${vialData[idx]['dateDeposited']}
        <span>
      `

      // Listen to mouse hover event, then add data to vialInfo
      vialCell.addEventListener("mouseover", renderDetails = () => {
        vialInfo.innerHTML = `
          <span class="info-field-title">Name</span> <br /> 
          ${vialData[idx]['longName']} <br /><br />
          
          <span class="info-field-title">Depositor</span> <br />
            ${vialData[idx]['vialDepositor']} on ${vialData[idx]['dateDeposited']} <br />
            ${vialData[idx]['vialMeta']}
          <br /><br />

          <span class="info-field-title">Origin</span> <br> 
            ${vialData[idx]['vialOrigin']} <br />
        `
      })

      // If the mouse is outside of the area, clear vialInfo
      vialCell.addEventListener("mouseout", clearDetails = () => {
        vialInfo.innerHTML = hoverTextContent
      })

      /*
      // commented on 2024-JUL-04
      // If the cell is click, copy longname to clipboard
      vialCell.addEventListener("click", copyToClipboard = () => {
        const spitOutName = vialData[idx]['longName']
        navigator.clipboard.writeText(spitOutName)
      })
      */

      // If the cell is clicked, open hovered window to show details
      // added on 2024-JUL-04
      vialCell.addEventListener("click", openVialDetail = () => {
        vialDetailsContainer = document.getElementById("vial-dialog")
        vialDetailsTopBar = document.getElementById("vial-dialog-topBarName")
        vialDetailsInfo = document.getElementById("vial-dialog-content")

        vialDetailsContainer.style.visibility = "visible"

        vialDetailsTopBar.innerHTML = `${vialData[idx]['Position']} // ${vialData[idx]['shortName']}`
        vialDetailsInfo.innerHTML = `
          <span class="info-field-title">Name</span> <br /> 
          ${vialData[idx]['longName']} <br /><br />

          <span class="info-field-title">Depositor</span> <br />
          ${vialData[idx]['vialDepositor']} on ${vialData[idx]['dateDeposited']} <br />
          ${vialData[idx]['vialMeta']}<br /><br />

          <span class="info-field-title">Origin</span> <br />
          ${vialData[idx]['vialOrigin']} <br />
        `
      })
    }
  })
}

// -----------------------------------------------------------------------------
// vial-dialog controls
const injectVialDialogDiv = () => {
  let vialDetails = document.createElement("div")
  vialDetails.setAttribute("id", "vial-dialog")
  vialDetails.innerHTML = `
    <div id="vial-dialog-topBar">
      <span id="vial-dialog-topBarName"></span>
      <span id="vial-dialog-closeButton">×</span>
    </div>
    <div id="vial-dialog-content"></div>
  `

  vialDetails.style.visibility = "hidden"
  document.body.appendChild(vialDetails)
}

const closeVialDialogDiv = () => {
  vialDetails = document.getElementById("vial-dialog")
  vialCloseButton = document.getElementById("vial-dialog-closeButton")

  vialCloseButton.addEventListener("click", closeDialog = () => {
    vialDetails.style.visibility = "hidden"
  })
}


// -----------------------------------------------------------------------------
// Execution layer!
labelCellPositions()
markCells()
injectVialDialogDiv()
closeVialDialogDiv()
