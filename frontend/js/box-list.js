const fetchBoxData = async () => {
  try {
    const response = await fetch(`${ ApiUrl }/boxes`)
    const data = await response.json()
    return data.data
  } catch (error) {
    console.error(error)
  }
}

const displayBoxInfo = async () => {
  let boxInfoDiv = document.getElementById('index_box_info')

  const insertBoxData = async(boxData) => {
    for (const box of boxData) {
      boxInfoDiv.innerHTML += `
        <div class="box_list_start">

          <div>
            <span class="box_label_title">
              <a href="/boxes/${ box.boxType }.html?box_id=${ box.BoxID }">${ box.BoxID }</a>
            </span>
            <span class="box_label_subtitle">${ box.boxDescription }</span>
          </div>
          <div>
          <span class="box_label_location">🧭 ${ box.storageLocation }</span>
          <span class="box_label_capacity">📦 ${ box.boxStatus } </span>
          </div>
          <div>
            <span class="box_label_lastItem">
              📥 Last item added: ${ box.recentlyAdded[0] } on ${ box.recentlyAdded[1] }
            </span>
          </div>

        </div>
      `
    }
  }

  let allBoxData = fetchBoxData()
  allBoxData.then(boxData => insertBoxData(boxData))
}



// Execution layer!
// -----------------------------------------------------------------------------
displayBoxInfo()
