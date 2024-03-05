<script>
  import { onMount } from "svelte";

  let medicine = '';
  let keywords = [""];
  let data = false;
  let brochure = false;
  let BASE_API_URL = "";
  let reponse_id = 0;

  // generate random number from 1-5
  const getRandomNumber = () => {
    return Math.floor(Math.random() * 4) + 1;
  };

  const handleGetResponses = async () => {
    reponse_id = getRandomNumber();
    let response_url = BASE_API_URL+ "responses/" + reponse_id + "/";
    console.log("here", response_url);
    data = false
    brochure = false
    const response = await fetch(response_url);
    data = await response.json();
    console.log(data);
    return;
  };

  const handleGetBrochure = async () => {
    let response_url = BASE_API_URL+ "local_brochure/" + reponse_id + "/";
    console.log("here", response_url);
    brochure = false
    const response = await fetch(response_url);
    brochure = await response.json();
    console.log(brochure);
    return;
  };

  onMount(() => {
    if (window.location.hostname.includes("localhost")){
      BASE_API_URL =
      window.location.protocol + "//" + window.location.hostname + ":8000/api/";
    } else {
      BASE_API_URL =window.location.protocol + "//" + window.location.hostname + "/api/";
    }
    console.log(BASE_API_URL);
  });
</script>

<main>
  <h1>Welcome to Pharma Pro Link (PPL)</h1>

  <div class="search">
    <div class="question">Which medicine are you working on and what are the keywords for search?</div>
    <label for="medicine">Medicine:</label>
    <input id="medicine" type="text" placeholder="e.g., Cosentyx" bind:value={medicine} />
    <label for="keywords">Keywords:</label>
    <input id="keywords" type="text" placeholder="e.g., psoriasis, ankylosing spondylitis"  bind:value={keywords}/>
    <button on:click|preventDefault={handleGetResponses}>Search</button>
  </div>

  <div class="response">
    {#if data && !brochure}
      <h2>Response</h2>
      <p>{@html data.response}</p>
      <h3>References</h3>
      <div class="references">
        {#each data.references as reference}
        <a href={reference.url}>{reference.title}<br/></a>
        {/each}
      </div>
      <!-- two buttons, one for new generation, another one for confirmation -->
      <button on:click|preventDefault={handleGetResponses}>This is wrong</button>
      <button on:click|preventDefault={handleGetBrochure}>I am happy</button>
    <!-- {:else}
      <h2>Response</h2>
      <p>Click on the search button to get the response</p> -->
    {/if}
  </div>

  <div class="brochure">
    {#if brochure}
      <h2>Brochure</h2>
      <p>{@html brochure.response}</p>
      <h3>References</h3>
      <div class="references">
        {#each brochure.references as reference}
          <a href={reference.url}>{reference.title}<br/></a>
        {/each}
      </div>
    <!-- {:else}
      <h2>Brochure</h2>
      <p>Click on the happy button to get the brochure</p> -->
    {/if}
  </div>
</main>

<style>
  p{
    white-space: pre-line;
    text-align: left;
  }

  .references {
    text-align: left;
  }
</style>
