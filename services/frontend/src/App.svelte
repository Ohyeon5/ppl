<script>
  let medicine = '';
  $: console.log('medicine:', medicine);
</script>

<main>
  <h1>Welcome to Pharma Pro Link (a.k.a. PPL)</h1>

  <div class="medicine-input">
    <label for="medicine">Which medicine are you working on?</label>
    <input id="medicine" type="text" placeholder="e.g., Cosentyx" bind:value={medicine} />
  </div>
</main>
