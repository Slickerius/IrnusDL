const socket = new WebSocket('wss://' + window.location.host + '/ws/download/');

socket.onmessage = (e) => {
  const data = JSON.parse(e.data);
  const stringifiedData = JSON.stringify(data, null, 2);

  if (data['status'] === 'INFO') {
    const albumArtUrl = data['album_art_url'];
    const albumArtist = data['album_artist'];
    const albumTitle = data['album_title'];
    let albumYear = data['album_year'];
    let albumCountry = data['album_country'];

    if (!albumYear)
      albumYear = '-';

    if (!albumCountry)
      albumCountry = '-';

    $('#albumInfoCard').removeClass('d-none');
    $('#albumInfoArtist').text(albumArtist);
    $('#albumInfoName').text(albumTitle);
    $('#albumInfoYear').text(albumYear);
    $('#albumInfoCountry').text(albumCountry);
    $('#albumInfoImg').attr('src', albumArtUrl);
  }

  if (data['status'] === 'PROCESS')
    $('#statusText').text(data['message']);
  
  if (data['status'] === 'SUCCESS') {
    $('#statusCard').removeClass('border-primary');
    $('#statusCard').addClass('border-success');
    $('#cardProcessingContent').removeClass('d-flex');
    $('#cardProcessingContent').addClass('d-none');
    $('#cardErrorContent').removeClass('d-flex');
    $('#cardErrorContent').addClass('d-none');
    $('#cardSuccessContent').removeClass('d-none');

    $('#fetchButton').off('click').click(() => {
      $.ajax({
        url: data['url'],
        type : 'HEAD',
        success: () => {
          window.location.href = data['url'];
        },
        error: () => { 
          $('#statusCard').removeClass('border-primary');
          $('#statusCard').addClass('border-danger');
          $('#cardProcessingContent').removeClass('d-flex');
          $('#cardProcessingContent').addClass('d-none');
          $('#cardSuccessContent').addClass('d-none');
          $('#cardErrorContent').removeClass('d-none');
          $('#cardErrorContent').addClass('d-flex');

          $('#errorText').text('File does not exist or has expired.');
        }
      }); 
    });
  }

  if (data['status'] === 'ERROR') {
    $('#statusCard').removeClass('border-primary');
    $('#statusCard').addClass('border-danger');
    $('#cardProcessingContent').removeClass('d-flex');
    $('#cardProcessingContent').addClass('d-none');
    $('#cardSuccessContent').addClass('d-none');
    $('#cardErrorContent').removeClass('d-none');
    $('#cardErrorContent').addClass('d-flex');
    
    $('#errorText').text(data['message']);
  }
};

socket.onclose = (e) => {
  console.error('Chat socket closed unexpectedly');
};

const sendDownloadRequest = (url, isUseTrackArtist, isUseMultipleArtist) => {
  socket.send(JSON.stringify({
    'url': url,
    'is_use_track_artist': isUseTrackArtist,
    'is_use_multiple_artist': isUseMultipleArtist
  }));
};

$(document).ready(() => {
  $('#downloadButton').on('click', () => {
    $('#statusText').text('Loading...');

    $('#statusCard').removeClass('d-none');
    $('#statusCard').removeClass('border-success');
    $('#statusCard').removeClass('border-danger');
    $('#statusCard').addClass('border-primary');
    $('#cardProcessingContent').removeClass('d-none');
    $('#cardProcessingContent').addClass('d-flex');

    $('#cardErrorContent').addClass('d-none');
    $('#cardSuccessContent').addClass('d-none');

    const url = $('#downloadURL').val();
    const isUseTrackArtist = $('#useTrackArtistSwitch').is(':checked');
    const isUseMultipleArtist = $('#useMultipleArtistSwitch').is(':checked');

    sendDownloadRequest(url, isUseTrackArtist, isUseMultipleArtist);
  });
});
