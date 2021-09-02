//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; 						//stream from getUserMedia()
var recorder; 						//WebAudioRecorder object
var input; 							//MediaStreamAudioSourceNode  we'll be recording
var encodeAfterRecord = true;       // when to encode

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //new audio context to help us record

// var encodingTypeSelect = document.getElementById("encodingTypeSelect");
var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);

function startRecording() {
	console.log("startRecording() called");
  var constraints = { audio: true, video:false }

    /*
    	We're using the standard promise based getUserMedia() 
    	https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
	*/

	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		__log("getUserMedia() success, stream created, initializing WebAudioRecorder...");

		/*
			create an audio context after getUserMedia is called
			sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
			the sampleRate defaults to the one set in your OS for your playback device

		*/
		audioContext = new AudioContext();

		//update the format 
		// document.getElementById("formats").innerHTML="Format: 2 channel "+encodingTypeSelect.options[encodingTypeSelect.selectedIndex].value+" @ "+audioContext.sampleRate/1000+"kHz"
		// document.getElementById("formats").innerHTML="Format: 1 channel wav @ "+audioContext.sampleRate/1000+"kHz"

		//assign to gumStream for later use
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);
		
		//stop the input from playing back through the speakers
		//input.connect(audioContext.destination)

		//get language
		let lang = $('#langbox').val();

		//get scorer
		let scorer = $('#scorerbox').val();

		recorder = new WebAudioRecorder(input, {
		  workerDir: "/static/js/", // must end with slash
		  encoding: "wav",
		  numChannels:1, //2 is the default, mp3 encoding supports only 2
		  onEncoderLoading: function(recorder, encoding) {
		    // show "loading encoder..." display
		    // __log("Loading "+encoding+" encoder...");
		  },
		  onEncoderLoaded: function(recorder, encoding) {
		    // hide "loading encoder..." display
		    // __log(encoding+" encoder loaded");
		  }
		});

		recorder.onComplete = function(recorder, blob) { 
			// __log("Encoding complete");
			var url = URL.createObjectURL(blob);
			filename = new Date().toISOString() + '.'+recorder.encoding;
			createDownloadLink(url, filename, recorder.encoding);
			// encodingTypeSelect.disabled = false;
			var file = new File([blob], filename);
			let fd = new FormData();
		    fd.append('file', file);
		    fd.append('lang', lang);
		    fd.append('scorer', scorer);
		    console.log("file: ", file);
		    console.log("lang: ", lang);
		    console.log("scorer: ", scorer);
		    uploadData(fd);
		}

		recorder.setOptions({
		  timeLimit:120,
		  encodeAfterRecord:encodeAfterRecord,
	      ogg: {quality: 0.5},
	      mp3: {bitRate: 160}
	    });

		//start the recording process
		recorder.startRecording();

		 __log("Recording started");

	}).catch(function(err) {
	  	//enable the record button if getUSerMedia() fails
    	recordButton.disabled = false;
    	stopButton.disabled = true;

	});

	//disable the record button
    recordButton.disabled = true;
    stopButton.disabled = false;
}

function stopRecording() {
	console.log("stopRecording() called");
	
	//stop microphone access
	gumStream.getAudioTracks()[0].stop();

	//disable the stop button
	stopButton.disabled = true;
	recordButton.disabled = false;
	
	//tell the recorder to finish the recording (stop recording + encode the recorded audio)
	recorder.finishRecording();

	__log('Recording stopped');
}

function createDownloadLink(url,filename,encoding) {
	var au = document.createElement('audio');
	var li = document.createElement('li');
	var link = document.createElement('a');

	//add controls to the <audio> element
	au.controls = true;
	au.src = url;

	//link the a element to the blob
	link.href = url;
	link.download = filename;
	link.innerHTML = link.download;

	//add the new audio and a elements to the li element
	li.appendChild(au);
	li.appendChild(link);

	//add the li element to the ordered list
	// recordingsList.appendChild(li);

	$('#audiopanel').html(au);
}

// Logic for file uploading

$(function () {
  // dragdrop();

  function preparedata (file, lang, scorer) {
    const img = document.createElement("img");
    img.src = URL.createObjectURL(file);
    let fd = new FormData();
    fd.append('file', file);
    fd.append('lang', lang);
    fd.append('scorer', scorer);
    console.log("file: ", file);
    console.log("lang: ", lang);
    console.log("scorer: ", scorer);
    createDownloadLink(img.src, file, "wav");
    uploadData(fd);
  }

  function dotranscribe () {
    let imageType = /image.*/;
    let file = $('#file')[0].files[0];
    let lang = $('#langbox').val();
    let scorer = $('#scorerbox').val();
    preparedata(file, lang, scorer);
  }

  // file selected
  $("#file").change(dotranscribe);

  // // language changed
  // $("#langbox").change(dotranscribe);
});

// Sending AJAX request and upload file
function uploadData (formdata) {
  $.ajax({
    url: '/transcribe/new/',
    type: 'post',
    data: formdata,
    contentType: false,
    processData: false,
    success: function (data) {
      $("#result").html(data.text);
    }
  });
}

//helper function
function __log(e, data) {
	log.innerHTML += "\n" + e + " " + (data || '');
}