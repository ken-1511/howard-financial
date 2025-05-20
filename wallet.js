
async function connectWallet() {
  if (typeof window.ethereum !== 'undefined') {
    try {
      const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
      document.getElementById('walletAddress').innerText = accounts[0];
      document.getElementById('walletInfo').classList.remove('hidden');

      const chainId = await ethereum.request({ method: 'eth_chainId' });
      let network = '';
      switch (chainId) {
        case '0x89':
          network = 'Polygon Mainnet';
          break;
        case '0x1':
          network = 'Ethereum Mainnet';
          break;
        default:
          network = 'Other Network';
      }
      document.getElementById('networkInfo').innerText = `Detected Network: ${network}`;
    } catch (error) {
      console.error("Error connecting wallet:", error);
    }
  } else {
    alert("Please install MetaMask or another Web3 wallet extension.");
  }
}

document.getElementById('connectBtn').addEventListener('click', connectWallet);
