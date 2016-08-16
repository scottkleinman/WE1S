$(document).ready(function () {
    var today = moment().format('YYYY-MM-DD');
    var defaultData = {
        "description": "bortaS <b>bIr</b> jablu’DI’ reH QaQqu’ nay’!",
        "language": "en",
        "country": "usa",
        "namespace": "WE1Sv1.0",
        "date": {
            "start": today,
            "end": today
        }
    };

    $("#form").alpaca({
        "data": defaultData,
        "schema": {
            "title": "Publication Manifest Form",
            "type": "object",
            "properties": {
                "namespace": {
                    "enum": ["WE1Sv1.0"],
                    "label": "namespace",
                    "type": "string",
                    "required": true
                },
                "_id": {
                    "type": "string",
                    "title": "_id",
                    "required": true
                },
                "publication": {
                    "type": "string",
                    "title": "Publication",
                    "required": true
                },
                "path": {
                    "type": "string",
                    "title": "Path",
                    "required": true
                },
                "description": {
                    "type": "string",
                    "required": true
                },
                "publisher": {
                    "type": "string",
                    "title": "Publisher",
                    "required": false
                },
                "date": {
                    "title": "Publication Date",
                    "type": "object",
                    "required": true,
                    "properties": {
                        "start": {
                            "title": "Enter Start Date",
                            "format": "string"
                        },
                        "end": {
                            "title": "Enter End Date",
                            "format": "string"
                        }
                    }
                },
                "edition": {
                    "type": "string",
                    "title": "Edition"
                },
                "altTitle": {
                    "type": "string",
                    "title": "Alternative Title"
                },
                "contentType": {
                    "type": "string",
                    "title": "Content Type"
                },
                // ISO-639-2 language codes
                "language": {
                    "enum": ["aa", "ab", "af", "ak", "als", "am", "an", "ang", "ar", "arc", "as", "ast", "av", "ay", "az", "ba", "bar", "bat-smg", "bcl", "be", "be-x-old", "bg", "bh", "bi", "bm", "bn", "bo", "bpy", "br", "bs", "bug", "bxr", "ca", "cdo", "ce", "ceb", "ch", "cho", "chr", "chy", "co", "cr", "cs", "csb", "cu", "cv", "cy", "da", "de", "diq", "dsb", "dv", "dz", "ee", "far", "el", "en", "eo", "es", "et", "eu", "ext", "ff", "fi", "fiu-vro", "fj", "fo", "fr", "frp", "fur", "fy", "ga", "gan", "gd", "gil", "gl", "gn", "got", "gu", "gv", "ha", "hak", "haw", "he", "hi", "ho", "hr", "ht", "hu", "hy", "hz", "ia", "id", "ie", "ig", "ii", "ik", "ilo", "io", "is", "it", "iu", "ja", "jbo", "jv", "ka", "kg", "ki", "kj", "kk", "kl", "km", "kn", "khw", "ko", "kr", "ks", "ksh", "ku", "kv", "kw", "ky", "la", "lad", "lan", "lb", "lg", "li", "lij", "lmo", "ln", "lo", "lt", "lv", "map-bms", "mg", "man", "mh", "mi", "min", "mk", "ml", "mn", "mo", "mr", "ms", "mt", "mus", "my", "na", "nah", "nap", "nd", "nds", "nds-nl", "ne", "new", "ng", "nl", "nn", "no", "nr", "nso", "nrm", "nv", "ny", "oc", "oj", "om", "or", "os", "pa", "pag", "pam", "pap", "pdc", "pi", "pih", "pl", "pms", "ps", "pt", "qu", "rm", "rmy", "rn", "ro", "roa-rup", "ru", "rw", "sa", "sc", "scn", "sco", "sd", "se", "sg", "sh", "si", "simple", "sk", "sl", "sm", "sn", "so", "sq", "sr", "ss", "st", "su", "sv", "sw", "ta", "te", "tet", "tg", "th", "ti", "tk", "tl", "tlh", "tn", "to", "tpi", "tr", "ts", "tt", "tum", "tw", "ty", "udm", "ug", "uk", "ur", "uz", "ve", "vi", "vec", "vls", "vo", "wa", "war", "wo", "xal", "xh", "yi", "yo", "za", "zh", "zh-classical", "zh-min-nan", "zh-yue", "zu"],
                    "title": "Language",
                    "required": true
                },
                // ISO country codes
                "country": {
                    "type": "string",
                    "title": "Country",
                    "required": true
                },
                "authors": {
                    "type": "array",
                    "title": "Authors",
                    // Add "Author Name" legend to subfields
                    "items": {
                        "title": "Author Name",
                        "type": "string"
                    }
                },
                "notes": {
                    "type": "array",
                    "title": "Notes"
                }
            }
        },
        "options": {
            "hideInitValidationError": true,
            "form": {
                "attributes": {
                    "action": document.URL,
                    "method": "post"
                },
                "buttons": {
                    "submit": {
                        "title": "Submit",
                        "click": function () {
                            // Somewhat elaborate procedure to turn the json into a string
                            var value = this.getValue();
                            // Submit data by Ajax
                            $.ajax({
                                type: "POST",
                                url: document.URL,
                                data: JSON.stringify(value),
                                contentType: 'application/json',
                                dataType: 'json',
                                beforeSend: function () {
                                    console.log(JSON.stringify(value, null, "\t"));
                                },
                                success: function (jsonResult) {
                                    console.log(jsonResult);
                                    // Remove the html list from the json response and send
                                    // it to the modal
                                    var htmlResult = jsonResult["htmlResult"];
                                    delete jsonResult["htmlResult"];
                                    $('.modal-body').html(htmlResult);
                                    $('#myModal').modal();
                                },
                                error: function (jqXHR, textStatus, errorThrown) {
                                    $('.modal-body').html('Error: Your action could not be completed.');
                                    $('#myModal').modal();
                                    console.log("Error: " + errorThrown);
                                }
                            });
                        }
                    }
                }
            },
            // Field configuration arrray
            "fields": {
                "namespace": {
                    "type": "select"
                },
                "_id": {
                    // Remove initial 'The', replace space with "_"; remove error styling
                    "onFieldKeyup": function (e) {
                        var v = this.getValue();
                        v = v.replace(/The /g, "");
                        v = v.toLowerCase();
                        v = v.replace(/\s+/g, "_");
                        $('input[name="_id"]').val(v);
                        var idDiv = $("div").find('[data-alpaca-field-name="_id"]');
                        idDiv.removeClass("alpaca-required has-error alpaca-invalid");
                    }
                },
                "publication": {
                    // On change, remove initial "The", replace whitespace with "_", send value to _id,
                    // remove error styling
                    "events": {
                        "change": function () {
                            var p = $('input[name="publication"]').val();
                            p = p.replace(/The /g, "");
                            p = p.toLowerCase();
                            p = p.replace(/\s+/g, "_");
                            $('input[name="_id"]').val(p);
                            var idDiv = $("div").find('[data-alpaca-field-name="_id"]');
                            idDiv.removeClass("alpaca-required has-error alpaca-invalid");
                        }
                    }
                },
                "path": {
                    // Change comma to slash at any keystroke
                    "onFieldKeyup": function (e) {
                        var v = this.getValue();
                        v = v.replace(/,/g, "/");
                        $('input[name="path"]').val(v);
                    },
                    "events": {
                        // On change, ensure that the string begins "/Publications/"
                        "change": function () {
                            var v = this.getValue();
                            if (v.substring(0, 14) != "/Publications/") {
                                v = "/Publications/" + v;
                                $('input[name="path"]').val(v)
                            }
                            if (v.substring(-1) != "/") {
                                $('input[name="path"]').val(v + "/")
                            }
                        }
                    }
                },
                // Add CKEditor with basic html tools
                "description": {
                    "type": "ckeditor",
                    "ckeditor": {
                        "toolbar": [
                            ['Bold', 'Italic', 'Underline', 'StrikeThrough', '-', 'Undo', 'Redo', '-', 'Cut', 'Copy', 'Paste', 'Find', 'Replace', '-', 'Outdent', 'Indent', '-', 'Print'], '/', ['NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
                            ['Image', 'Table', '-', 'Link', 'Flash', 'TextColor', 'BGColor', 'Source']
                        ]
                    }
                },
                "date": {
                    "fields": {
                        "start": {
                            // Enter today's date in the datepicker; use YYYY-DD-MM format; allow manual entry
                            "type": "date",
                            "picker": {
                                "format": "YYYY-MM-DD",
                                "useCurrent": true
                            },
                            "event": {
                                "change": function () {
                                    var end = new Date($('input[name="end"]').val());
                                    console.log(end);
                                }
                            }
                        },
                        "end": {
                            // Enter today's date in the datepicker; use YYYY-DD-MM format; allow manual entry
                            "type": "date",
                            "picker": {
                                "format": "YYYY-MM-DD",
                                "useCurrent": true
                            }
                        }
                    }
                },
                // ISO-639 Language labels
                "language": {
                    "optionLabels": ["Afar", "Abkhazian", "Afrikaans", "Akan", "Alemannic", "Amharic", "Aragonese", "Anglo-Saxon / Old English", "Arabic", "Aramaic", "Assamese", "Asturian", "Avar", "Aymara", "Azerbaijani", "Bashkir", "Bavarian", "Samogitian", "Bikol", "Belarusian", "Belarusian (Taraškievica)", "Bulgarian", "Bihari", "Bislama", "Bambara", "Bengali", "Tibetan", "Bishnupriya Manipuri", "Breton", "Bosnian", "Buginese", "Buriat (Russia)", "Catalan", "Min Dong Chinese", "Chechen", "Cebuano", "Chamorro", "Choctaw", "Cherokee", "Cheyenne", "Corsican", "Cree", "Czech", "Kashubian", "Old Church Slavonic / Old Bulgarian", "Chuvash", "Welsh", "Danish", "German", "Dimli", "Lower Sorbian", "Divehi", "Dzongkha", "Ewe", "Farsi", "Greek", "English", "Esperanto", "Spanish", "Estonian", "Basque", "Extremaduran", "Peul", "Finnish", "Võro", "Fijian", "Faroese", "French", "Arpitan / Franco-Provençal", "Friulian", "West Frisian", "Irish", "Gan Chinese", "Scottish Gaelic", "Gilbertese", "Galician", "Guarani", "Gothic", "Gujarati", "Manx", "Hausa", "Hakka Chinese", "Hawaiian", "Hebrew", "Hindi", "Hiri Motu", "Croatian", "Haitian", "Hungarian", "Armenian", "Herero", "Interlingua", "Indonesian", "Interlingue", "Igbo", "Sichuan Yi", "Inupiak", "Ilokano", "Ido", "Icelandic", "Italian", "Inuktitut", "Japanese", "Lojban", "Javanese", "Georgian", "Kongo", "Kikuyu", "Kuanyama", "Kazakh", "Greenlandic", "Cambodian", "Kannada", "Khowar", "Korean", "Kanuri", "Kashmiri", "Ripuarian", "Kurdish", "Komi", "Cornish", "Kirghiz", "Latin", "Ladino / Judeo-Spanish", "Lango", "Luxembourgish", "Ganda", "Limburgian", "Ligurian", "Lombard", "Lingala", "Laotian", "Lithuanian", "Latvian", "Banyumasan", "Malagasy", "Mandarin", "Marshallese", "Maori", "Minangkabau", "Macedonian", "Malayalam", "Mongolian", "Moldovan", "Marathi", "Malay", "Maltese", "Creek / Muskogee", "Burmese", "Nauruan", "Nahuatl", "Neapolitan", "North Ndebele", "Low German / Low Saxon", "Dutch Low Saxon", "Nepali", "Newar", "Ndonga", "Dutch", "Norwegian Nynorsk", "Norwegian", "South Ndebele", "Northern Sotho", "Norman", "Navajo", "Chichewa", "Occitan", "Ojibwa", "Oromo", "Oriya", "Ossetian / Ossetic", "Panjabi / Punjabi", "Pangasinan", "Kapampangan", "Papiamentu", "Pennsylvania German", "Pali", "Norfolk", "Polish", "Piedmontese", "Pashto", "Portuguese", "Quechua", "Raeto Romance", "Romani", "Kirundi", "Romanian", "Aromanian", "Russian", "Rwandi", "Sanskrit", "Sardinian", "Sicilian", "Scots", "Sindhi", "Northern Sami", "Sango", "Serbo-Croatian", "Sinhalese", "Simple English", "Slovak", "Slovenian", "Samoan", "Shona", "Somalia", "Albanian", "Serbian", "Swati", "Southern Sotho", "Sundanese", "Swedish", "Swahili", "Tamil", "Telugu", "Tetum", "Tajik", "Thai", "Tigrinya", "Turkmen", "Tagalog ", "Klingon", "Tswana", "Tonga", "Tok Pisin", "Turkish", "Tsonga", "Tatar", "Tumbuka", "Twi", "Tahitian", "Udmurt", "Uyghur", "Ukrainian", "Urdu", "Uzbek", "Venda", "Vietnamese", "Venetian", "West Flemish", "Volapük", "Walloon", "Waray-Waray / Samar-Leyte Visayan", "Wolof", "Kalmyk", "Xhosa", "Yiddish", "Yoruba", "Zhuang", "Chinese", "Classical Chinese", "Minnan", "Cantonese", "Zulu"]
                },
                // ISO-language codes
                "country": {
                    "type": "country"
                },
                "authors": {
                    // Change add button text to "Add Author"
                    "toolbar": {
                        "showLabels": true,
                        "actions": [
                            {"label": "Add Author", "action": "add"}]
                    }
                },
                "notes": {
                    // Change add button text to "Add Note"
                    "toolbar": {
                        "showLabels": true,
                        "actions": [
                            {"label": "Add Note", "action": "add"}
                        ]
                    },
                    // Show full-sized buttons with labels in actionbar
                    "actionbar": {
                        "showLabels": true,
                        "actions": [
                            {"label": "Add Note", "action": "add"},
                            {"label": "Delete Note", "action": "remove"},
                            {"label": "Move Up", "action": "up"},
                            {"label": "Move Down", "action": "down"}
                        ]
                    }
                }
            } // End fields
        },// End options
        "postRender": function (control) {
            var start = control.childrenByPropertyId["date"].childrenByPropertyId["start"];
            var end = control.childrenByPropertyId["date"].childrenByPropertyId["end"];
            end.subscribe(start, function (val) {
                var endDate = new Date($('input[name="date_end"]').val());
                var startDate = new Date(val);
                if (endDate < startDate) {
                    end.setValue(val);
                }
            });
        }
    });
});